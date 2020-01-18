import os
import re
import subprocess
import uuid
from typing import Optional, Tuple

from touchstone import common
from touchstone.lib import exceptions


class RunResult(object):
    def __init__(self, container_id, port, ui_port=None):
        self.container_id = container_id
        self.port = port
        self.ui_port = ui_port


class DockerManager(object):
    def __init__(self, should_auto_discover: bool = True):
        self.__images: list = []
        self.__containers: list = []
        self.__should_auto_discover = should_auto_discover

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

    def run_image(self, image: str, port_mapping: Tuple[int, int], ui_port_mapping: Tuple[int, int] = None,
                  environment_vars: list = None) -> RunResult:
        if environment_vars is None:
            environment_vars = []
        additional_params = ''

        port = port_mapping[0]
        ui_port = ui_port_mapping[0] if ui_port_mapping else None

        if self.__should_auto_discover:
            additional_params += f' -p :{port_mapping[1]}'
        else:
            additional_params += f' -p {port}:{port_mapping[1]}'
        if ui_port_mapping:
            if self.__should_auto_discover:
                additional_params += f' -p :{ui_port_mapping[1]}'
            else:
                additional_params += f' -p {ui_port}:{ui_port_mapping[1]}'

        for var, value in environment_vars:
            value = common.replace_host_with_docker_equivalent(str(value))
            additional_params += f' -e {var}="{value}"'

        container_id = uuid.uuid4().hex
        command = f'docker run -d --name {container_id}{additional_params} {image}'
        common.logger.info(f'Running container with command: {command}')
        result = subprocess.run(command, shell=True, stdout=subprocess.DEVNULL)

        if result.returncode is not 0:
            raise exceptions.ContainerException(
                f'Container image {image} could not be started. Ensure Docker is running and app port: '
                f'"{port_mapping[0]}" and service port: "{ui_port_mapping[0] if ui_port_mapping else "N/A"}" '
                f'are not already in use.')

        if self.__should_auto_discover:
            result = str(subprocess.run(['docker', 'port', container_id], stdout=subprocess.PIPE).stdout,
                         encoding='utf-8')
            for line in result.splitlines():
                container_port = int(re.search('.+?(?=/)', line).group())
                new_port = int(re.search('(?<=0.0.0.0:)\\d*', line).group())
                if container_port == port_mapping[1]:
                    port = new_port
                elif container_port == ui_port_mapping[1]:
                    ui_port = new_port

        self.__containers.append(container_id)
        return RunResult(container_id, port, ui_port)

    def stop_container(self, id):
        common.logger.info(f'Stopping container: {id}')
        subprocess.run(['docker', 'container', 'stop', id], stdout=subprocess.DEVNULL)
        common.logger.info(f'Removing container: {id}')
        subprocess.run(['docker', 'container', 'rm', id], stdout=subprocess.DEVNULL)
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
                common.logger.info(f'Removing container: {container}')
                subprocess.run(['docker', 'container', 'rm', container], stdout=subprocess.DEVNULL)
        self.__containers = []

    def containers_running(self) -> bool:
        return len(self.__containers) > 0
