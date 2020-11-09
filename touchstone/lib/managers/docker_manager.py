import os
import re
import subprocess
import uuid
from typing import Optional, Tuple, List

from touchstone import common
from touchstone.lib import exceptions


class RunResult(object):
    def __init__(self, container_id, internal_port, external_port, ui_port):
        self.container_id = container_id
        self.internal_port = internal_port
        self.external_port = external_port
        self.ui_port = ui_port


class DockerManager(object):
    def __init__(self, should_auto_discover: bool = True):
        self.__images: list = []
        self.__containers: list = []
        self.__should_auto_discover = should_auto_discover
        self.__network: Optional[str] = None

    def build_dockerfile(self, dockerfile_path: str) -> str:
        # Build context will always be the same location as the Dockerfile for our purposes
        build_context = os.path.dirname(dockerfile_path)
        tag = uuid.uuid4().hex
        command = f'docker build -t {tag} -f {dockerfile_path} {build_context}'
        common.logger.debug(f'Building Dockerfile with command: {command}')
        result = subprocess.run(command, shell=True)
        if result.returncode is not 0:
            raise exceptions.ContainerException(f'An error occurred while building Dockerfile: "{dockerfile_path}".')
        self.__images.append(tag)
        return tag

    def run_background_image(self, image: str, port: int = None, exposed_port: int = None, ui_port: int = None,
                             environment_vars: List[Tuple[str, str]] = [], options: str = None) -> RunResult:
        exposed_port = port if not exposed_port else exposed_port
        self.__create_network()

        additional_params = self.__build_ports_str(port, exposed_port, ui_port)
        if len(environment_vars) != 0:
            additional_params += ' '
            additional_params += self.__build_env_str(environment_vars)
        if options:
            additional_params += ' '
            additional_params += options

        container_id = self.__run_image(additional_params, image)

        # Extract the auto-discovered ports
        exposed_port = self.__extract_port_mapping(container_id, port)
        ui_port = self.__extract_port_mapping(container_id, ui_port)

        self.__containers.append(container_id)
        return RunResult(container_id, port, exposed_port, ui_port)

    def run_foreground_image(self, image: str, bind_mount: str, environment_vars: List[Tuple[str, str]] = [],
                             log_path: str = None, options: str = None):
        self.__create_network()
        additional_params = f'-v {bind_mount}'
        if len(environment_vars) != 0:
            additional_params += ' '
            additional_params += self.__build_env_str(environment_vars)
        if options:
            additional_params += ' '
            additional_params += options
        self.__execute_image(image, additional_params, log_path)

    def __create_network(self):
        if not self.__network:
            self.__network = uuid.uuid4().hex
            common.logger.debug(f'Creating network: {self.__network}')
            subprocess.run(['docker', 'network', 'create', self.__network], stdout=subprocess.DEVNULL)

    def __build_ports_str(self, port: int, exposed_port: int, ui_port: int) -> str:
        additional_params = ''
        if port:
            if self.__should_auto_discover:
                additional_params += f' -p :{port}'
            else:
                additional_params += f' -p {exposed_port}:{port}'
            additional_params += f' --expose {port}'
        if ui_port:
            additional_params += f' -p :{ui_port}'
        return additional_params[1:]

    def __build_env_str(self, environment_vars: List[Tuple[str, str]] = []) -> str:
        additional_params = ''
        for var, value in environment_vars:
            additional_params += f' -e {var}="{value}"'
        return additional_params[1:]

    def __run_image(self, additional_params: str, image: str) -> str:
        container_id = uuid.uuid4().hex
        command = f'docker run --rm -d --network {self.__network} '
        command += f'--name {container_id} {additional_params} {image}'
        common.logger.debug(f'Running container with command: {command}')
        result = subprocess.run(command, shell=True, stdout=subprocess.DEVNULL)
        if result.returncode is not 0:
            raise exceptions.ContainerException(
                f'Container image {image} could not be started. Ensure Docker is running and ports are not already in '
                f'use.')
        return container_id

    def __execute_image(self, image: str, additional_params: str, log_path: Optional[str]):
        command = f'docker run --rm --network {self.__network} '
        command += f'{additional_params} {image}'
        common.logger.debug(f'Executing container with command: {command}')
        if log_path:
            with open(log_path, 'w') as file:
                result = subprocess.run(command, shell=True, stdout=file)
        else:
            result = subprocess.run(command, shell=True)
        if result.returncode is not 0:
            raise exceptions.ContainerException(f'Container finished execution with non-zero return code.')

    def __extract_port_mapping(self, container_id: str, given_port: int) -> int:
        result = str(subprocess.run(['docker', 'port', container_id], stdout=subprocess.PIPE).stdout,
                     encoding='utf-8')
        for line in result.splitlines():
            found_port = int(re.search('.+?(?=/)', line).group())
            new_port = int(re.search('(?<=0.0.0.0:)\\d*', line).group())
            if found_port == given_port:
                return new_port
        return given_port

    def stop_container(self, id: str, log_path: str = None):
        if log_path:
            common.logger.debug(f'Writing container logs: {log_path}')
            with open(log_path, 'w') as file:
                subprocess.run(['docker', 'container', 'logs', id], stdout=file)
        common.logger.debug(f'Stopping container: {id}')
        subprocess.run(['docker', 'container', 'stop', id], stdout=subprocess.DEVNULL)
        self.__containers.remove(id)

    def cleanup(self):
        if self.__images:
            for image in self.__images:
                common.logger.debug(f'Removing image: {image}')
                subprocess.run(['docker', 'image', 'rm', image], stdout=subprocess.DEVNULL)
            self.__images = []
        if self.__containers:
            for container in self.__containers:
                common.logger.debug(f'Stopping container: {container}')
                subprocess.run(['docker', 'container', 'stop', container], stdout=subprocess.DEVNULL)
            self.__containers = []
        if self.__network:
            subprocess.run(['docker', 'network', 'rm', self.__network], stdout=subprocess.DEVNULL)
            self.__network = None

    def containers_running(self) -> bool:
        return len(self.__containers) > 0
