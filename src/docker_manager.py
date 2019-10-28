import subprocess
import uuid


class DockerManager:
    __instance = None

    @staticmethod
    def instance():
        if DockerManager.__instance is None:
            DockerManager()
        return DockerManager.__instance

    def __init__(self):
        DockerManager.__instance = self
        self.images = []
        self.containers = []

    def build_dockerfile(self, dockerfile_path):
        if dockerfile_path.endswith('Dockerfile'):
            dockerfile_path = dockerfile_path[:-10]
        tag = uuid.uuid4().hex
        result = subprocess.run(['docker', 'build', '-t', tag, dockerfile_path], stdout=subprocess.DEVNULL)
        if result.returncode is not 0:
            return None
        self.images.append(tag)
        return tag

    def run_image(self, image, exposed_port, container_port, dev_ports=None):
        additional_params = ''

        if dev_ports is not None:
            for dev_port in dev_ports:
                additional_params += f' -p {dev_port}:{dev_port}'

        name = uuid.uuid4().hex
        command = f'docker run -d --name {name} -p {exposed_port}:{container_port} {additional_params} {image}'
        subprocess.run(command, shell=True, stdout=subprocess.DEVNULL)

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
