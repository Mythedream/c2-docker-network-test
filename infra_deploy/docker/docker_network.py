import docker

from docker_container import DockerContainer

class DockerNetwork:
    def __init__(self, network_name, driver = "bridge", options = None):
        self.client = docker.from_env()
        self.network_name = network_name
        self.driver = driver
        self.options = options if options is not None else {}
        self.network = None

    def create_network(self):
        print(f"Creating network: {self.network_name}...")
        self.network = self.client.networks.create(
            self.network_name,
            driver = self.driver,
            options = self.options
        )
    
    def get_network_name(self) -> str:
        return self.network_name

    def inspect_network(self):
        if self.network:
            return self.network.attrs
        
    def connect_container_to_network(self, container: DockerContainer):
        if self.network and container:
            self.network.connect(container)

    def disconnect_container_from_network(self, container: DockerContainer):
        if self.network and container:
            self.network.disconnect(container)

    def remove_network(self):
        print(f"Removing network: {self.network_name}...")
        if self.network:
            self.network.remove()

if __name__ == "__main__":
    docker_network = DockerNetwork("my_network")
    docker_network.create_network()
    print(docker_network.inspect_network())
    docker_network.remove_network()    