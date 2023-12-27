import docker

class DockerContainer:
    def __init__(self, image_name: str, container_name: str, ports: dict = None, volumes: dict = None):
        print("Creating Docker manager:")
        self.client = docker.from_env()
        print(f"\tImage name: {image_name}")
        self.image_name = image_name
        print(f"\tContainer name: {container_name}")
        self.container_name = container_name
        print(f"\tPorts: {ports}")
        self.ports = ports if ports is not None else {}
        print(f"Volumes: {volumes}")
        self.volumes = volumes if volumes is not None else {}
        self.container = None

    def build_container(self):
        print(f"Building container: {self.container_name}...")
        self.container = self.client.containers.create(
            self.image_name,
            name = self.container_name,
            ports = self.ports,
            volumes = self.volumes
        )

    def run_container(self):
        print(f"Running container: {self.container_name}")
        if self.container:
            self.container.start()
        elif not self.container:
            self.build_container()
            self.run_container()

    def stop_container(self):
        print(f"Stopping container: {self.container_name}")
        if self.container:
            self.container.stop()

    def remove_container(self):
        print(f"Removing container: {self.container_name}")
        if self.container:
            self.container.remove()

    def get_container_name(self) -> str:
        return self.container_name


if __name__ == "__main__":
    image_name = "python:3.9-slim"
    container_name = "test_container"
    open_ports = {"80/tcp": 8080}
    docker_container = DockerContainer(
        image_name = image_name,
        container_name = container_name,
        ports = open_ports
    )
    docker_container.build_container()
    docker_container.run_container()

    docker_container.stop_container()
    docker_container.remove_container()
