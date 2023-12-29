from dataclasses import dataclass, field
import logging
from typing import Dict, Optional
from docker_network import DockerNetwork

@dataclass
class DockerNetworkManager:
    networks: Dict[str, DockerNetwork] = field(default_factory=dict)
    logger: logging.Logger = field(default=logging.getLogger("DockerNetworkManager"))

    def add_network(self, network_name: str, docker_network: DockerNetwork) -> bool:
        if network_name in self.networks:
            self.logger.warning(f"Network {network_name} already exists in the manager.")
            return False
        self.networks[network_name] = docker_network
        self.logger.info(f"Added network {network_name} to the manager.")
        return True

    def remove_network(self, network_name: str) -> bool:
        if network_name not in self.networks:
            self.logger.warning(f"Network {network_name} not found in the manager.")
            return False
        self.networks.pop(network_name)
        self.logger.info(f"Removed network {network_name} from the manager.")
        return True

    def get_network(self, network_name: str) -> Optional[DockerNetwork]:
        return self.networks.get(network_name)

    def create_all_networks(self):
        for network_name, network in self.networks.items():
            network.create_network()
            self.logger.info(f"Created network {network_name}.")

    def remove_all_networks(self):
        for network_name, network in self.networks.items():
            network.remove_network()
            self.logger.info(f"Removed network {network_name}.")