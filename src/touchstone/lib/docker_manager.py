import os
import subprocess
import uuid
from typing import Optional

from touchstone import common
from touchstone.lib import exceptions


class DockerManager(object):
    __instance: 'DockerManager' = None

    @staticmethod
    def instance() -> 'DockerManager':
        if DockerManager.__instance is None:
            DockerManager()
        return DockerManager.__instance

    def __init__(self):
        DockerManager.__instance = self
        self.__images: list = []
        self.__containers: list = []

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

    def run_image(self, image: str, ports: list) -> str:
        additional_params = ''

        for host, container in ports:
            additional_params += f' -p {host}:{container}'

        name = uuid.uuid4().hex
        command = f'docker run -d --name {name}{additional_params} {image}'
        common.logger.info(f'Running container with command: {command}')
        result = subprocess.run(command, shell=True, stdout=subprocess.DEVNULL)

        if result.returncode is not 0:
            exposed_ports = []
            for host, container in ports:
                exposed_ports.append(host)
            raise exceptions.ContainerException(
                f'Container image {image} could not be started. Ensure Docker is running and ports {exposed_ports} '
                f'are not already in use.')
        self.__containers.append(name)
        return name

    def stop_container(self, name):
        common.logger.info(f'Stopping container: {name}')
        subprocess.run(['docker', 'container', 'stop', name], stdout=subprocess.DEVNULL)
        common.logger.info(f'Removing container: {name}')
        subprocess.run(['docker', 'container', 'rm', name], stdout=subprocess.DEVNULL)
        self.__containers.remove(name)

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
