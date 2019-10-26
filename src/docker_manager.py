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

    def run_image(self, image, port=None):
        name = ''
        chosen_port = port

        if port is not None:
            current_port = port
            did_find_port = False
            tries = 0
            while not did_find_port and tries is not 5:
                name = uuid.uuid4().hex
                command = f'docker run -d --name {name} -p {current_port}:{port} {image}'
                result = subprocess.run(command, shell=True, stdout=subprocess.DEVNULL)
                if result.returncode is 0:
                    did_find_port = True
                else:
                    tries += 1
                    current_port += 1
            chosen_port = current_port
        else:
            name = uuid.uuid4().hex
            command = f'docker run -d --name {name} {image}'
            subprocess.run(command, stdout=subprocess.DEVNULL)

        self.containers.append(name)
        return chosen_port

    def cleanup(self):
        if self.images:
            subprocess.run(['docker', 'image', 'rm', ' '.join(self.images)], stdout=subprocess.DEVNULL)
        if self.containers:
            subprocess.run(['docker', 'container', 'stop', ' '.join(self.containers)], stdout=subprocess.DEVNULL)
            subprocess.run(['docker', 'container', 'rm', ' '.join(self.containers)], stdout=subprocess.DEVNULL)
