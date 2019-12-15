import os
import subprocess
import uuid
from typing import Optional

from touchstone.lib import exceptions


class DockerManager:
    __instance = None

    @staticmethod
    def instance():
        if DockerManager.__instance is None:
            DockerManager()
        return DockerManager.__instance

    def __init__(self):
        DockerManager.__instance = self
        self.images: list = []
        self.containers: list = []

    def build_dockerfile(self, dockerfile_path: str) -> Optional[str]:
        # Build context will always be the same location as the Dockerfile for our purposes
        build_context = os.path.dirname(dockerfile_path)
        tag = uuid.uuid4().hex
        result = subprocess.run(['docker', 'build', '-t', tag, '-f', dockerfile_path, build_context],
                                stdout=subprocess.DEVNULL)
        if result.returncode is not 0:
            return None
        self.images.append(tag)
        return tag

    def run_image(self, image: str, ports: list) -> str:
        additional_params = ''

        for host, container in ports:
            additional_params += f' -p {host}:{container}'

        name = uuid.uuid4().hex
        command = f'docker run -d --name {name} {additional_params} {image}'
        result = subprocess.run(command, shell=True, stdout=subprocess.DEVNULL)

        if result.returncode is not 0:
            exposed_ports = []
            for host, container in ports:
                exposed_ports.append(host)
            raise exceptions.ContainerException(
                f'Container image {image} could not be started. Ensure Docker is running and ports {exposed_ports} '
                f'are not already in use.')
        self.containers.append(name)
        return name

    def cleanup(self):
        if self.images:
            for image in self.images:
                subprocess.run(['docker', 'image', 'rm', image], stdout=subprocess.DEVNULL)
        if self.containers:
            for container in self.containers:
                subprocess.run(['docker', 'container', 'stop', container], stdout=subprocess.DEVNULL)
                subprocess.run(['docker', 'container', 'rm', container], stdout=subprocess.DEVNULL)
