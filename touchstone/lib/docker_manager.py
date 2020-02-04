import os
import re
import subprocess
import uuid
from typing import Optional, Tuple, List

from touchstone import common
from touchstone.lib import exceptions


class RunResult(object):
    def __init__(self, container_id, internal_port, external_port, ui_port=None):
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

    def build_dockerfile(self, dockerfile_path: str) -> Optional[str]:
        # Build context will always be the same location as the Dockerfile for our purposes
        build_context = os.path.dirname(dockerfile_path)
        tag = uuid.uuid4().hex
        command = f'docker build -t {tag} -f {dockerfile_path} {build_context}'
        common.logger.info(f'Building Dockerfile with command: {command}')
        result = subprocess.run(command, shell=True, stdout=subprocess.DEVNULL)
        if result.returncode is not 0:
            return None
        self.__images.append(tag)
        return tag

    def run_image(self, image: str, port: int = None, exposed_port: int = None, ui_port: int = None,
                  environment_vars: List[Tuple[str, str]] = []) -> RunResult:
        exposed_port = port if not exposed_port else exposed_port

        # Create network
        if not self.__network:
            self.__network = uuid.uuid4().hex
            common.logger.info(f'Creating network: {self.__network}')
            subprocess.run(['docker', 'network', 'create', self.__network], stdout=subprocess.DEVNULL)

        # Port setup
        additional_params = ''
        if port:
            if self.__should_auto_discover:
                additional_params += f' -p :{port}'
            else:
                additional_params += f' -p {exposed_port}:{port}'
            additional_params += f' --expose {port}'
        if ui_port:
            additional_params += f' -p :{ui_port}'

        # Environment variables setup
        for var, value in environment_vars:
            additional_params += f' -e {var}="{value}"'

        # Run the container
        container_id = uuid.uuid4().hex
        command = f'docker run --rm -d --network {self.__network} --name {container_id}{additional_params} {image}'
        common.logger.info(f'Running container with command: {command}')
        result = subprocess.run(command, shell=True, stdout=subprocess.DEVNULL)
        if result.returncode is not 0:
            raise exceptions.ContainerException(
                f'Container image {image} could not be started. Ensure Docker is running and port: "{exposed_port}" is '
                f'not already in use.')

        # Extract the auto-discovered ports
        result = str(subprocess.run(['docker', 'port', container_id], stdout=subprocess.PIPE).stdout,
                     encoding='utf-8')
        for line in result.splitlines():
            given_port = int(re.search('.+?(?=/)', line).group())
            discovered_port = int(re.search('(?<=0.0.0.0:)\\d*', line).group())
            if given_port == port:
                exposed_port = discovered_port
            elif given_port == ui_port:
                ui_port = discovered_port

        self.__containers.append(container_id)
        return RunResult(container_id, port, exposed_port, ui_port)

    def stop_container(self, id):
        common.logger.info(f'Stopping container: {id}')
        subprocess.run(['docker', 'container', 'stop', id], stdout=subprocess.DEVNULL)
        self.__containers.remove(id)

    def cleanup(self):
        if self.__images:
            for image in self.__images:
                common.logger.info(f'Removing image: {image}')
                subprocess.run(['docker', 'image', 'rm', image], stdout=subprocess.DEVNULL)
        self.__images = []
        if self.__containers:
            for container in self.__containers:
                common.logger.info(f'Stopping container: {container}')
                subprocess.run(['docker', 'container', 'stop', container], stdout=subprocess.DEVNULL)
        self.__containers = []
        if self.__network:
            subprocess.run(['docker', 'network', 'rm', self.__network], stdout=subprocess.DEVNULL)
            self.__network = None

    def containers_running(self) -> bool:
        return len(self.__containers) > 0
