from dataclasses import dataclass, field
import docker
import logging

@dataclass
class DockerNetwork:
    client: docker.DockerClient = field(default_factory=docker.from_env())
    logger: logging.Logger = field(default=logging.getLogger("DockerNetwork"))
    network_name: str
    network_id: str = field(init=False, default=None)

    def get_network_name(self) -> str:
        return self.network_name

    def create_network(self, 
               driver:str = "bridge", 
               check_duplicate: bool = True,
               interal: bool = False,
               attachable: bool = False,
               ingress: bool = False,
               ipam: dict = None,
               enable_ipv6: bool = False,
               labels: dict = None,
               options: dict = None
               ):
        try:

            self.logger.info(f"Creating network '{self.get_network_name()}' with driver '{driver}'...")
            network = self.client.networks.create(
                self.network_name,
                driver = driver,
                check_duplicate = check_duplicate,
                interal = interal,
                attachable = attachable,
                ingress = ingress,
                ipam = ipam,
                enable_ipv6 = enable_ipv6,
                labels = labels,
                options = options
            )
            self.network_id = network.id
            self.logger.info(f"Network '{self.network_name}' created.")
            return True
        except docker.errors.APIError as e:
            self.logger.error(f"API Error: {e}")

    def inspect(self):
        if self.network_id:
            try:
                network = self.client.networks.get(self.network_id)
                return network.attrs
            except docker.errors.NotFound:
                self.logger.error("Network not found.")
            except docker.errors.APIError as e:
                self.logger.error(f"API error: {e}")
        else:
            self.logger.warning("Network has not been created yet.")
        return None

    def connect_container(self, container_id: str):
        if self.network_id:
            try:
                network = self.client.networks.get(self.network_id)
                network.connect(container_id)
                self.logger.info(f"Connected container '{container_id}' to network '{self.network_name}'.")
                return True
            except docker.errors.NotFound:
                self.logger.error("Network or container not found.")
            except docker.errors.APIError as e:
                self.logger.error(f"API error: {e}")
        else:
            self.logger.warning("Network has not been created yet.")
        return False

    def disconnect_container(self, container_id: str):
        if self.network_id:
            try:
                network = self.client.networks.get(self.network_id)
                network.disconnect(container_id)
                self.logger.info(f"Disconnected container '{container_id}' from network '{self.network_name}'.")
                return True
            except docker.errors.NotFound:
                self.logger.error("Network or container not found.")
            except docker.errors.APIError as e:
                self.logger.error(f"API error: {e}")
        else:
            self.logger.warning("Network has not been created yet.")
        return False

    def remove_network(self):
        if self.network_id:
            try:
                network = self.client.networks.get(self.network_id)
                network.remove()
                self.logger.info(f"Network '{self.network_name}' removed.")
                self.network_id = None
                return True
            except docker.errors.NotFound:
                self.logger.error("Network not found.")
            except docker.errors.APIError as e:
                self.logger.error(f"API error: {e}")
        else:
            self.logger.warning("Network has not been created yet.")
        return False
    
    def list_connected_containers(self):
        if self.network_id:
            try:
                network = self.client.networks.get(self.network_id)
                return network.containers
            except docker.errors.NotFound:
                self.logger.error("Network not found.")
            except docker.errors.APIError as e:
                self.logger.error(f"API error: {e}")
        else:
            self.logger.warning("Network has not been created yet.")
        return []