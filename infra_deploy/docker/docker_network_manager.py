import json
import os
import glob

from docker_network import DockerNetwork
from docker_container_manager import DockerContainerManager

class DockerNetworkManager:
    def __init__(self, name: str):
        self.name = name
        self.networks = []

    def _is_valid_json_config(self, json_config_path):
        return os.path.exists(json_config_path)

    def add_network(self, network: DockerNetwork):
        print(f"Adding network '{network.network_name}' to list...")
        self.networks.append(network)

    def create_network(self, json_config_path):
        if not self._is_valid_json_config(json_config_path):
            raise ValueError("Invalid JSON configuration.")

        with open(json_config_path, "r") as json_file:
            data = json.load(json_file)

        network = DockerNetwork(
            network_name=data["network_name"],
            driver=data.get("driver", "bridge"),
            options=data.get("options", {})
        )

        network.create_network()
        self.add_network(network)

    def create_networks(self, config_directory="./network_configs"):
        base_path = os.path.dirname(__file__)
        full_config_path = os.path.join(base_path, config_directory)

        config_files = glob.glob(os.path.join(full_config_path, "*.json"))

        for config_file in config_files:
            try:
                self.create_network(config_file)
                print(f"Network created from {config_file}")
            except Exception as e:
                print(f"Failed to create network from {config_file}: {e}")

    def remove_network(self, network: DockerNetwork):
        print(f"Removing network: {network.network_name}")
        network.remove_network()

    def remove_networks(self):
        for network in self.networks:
            self.remove_network(network)

    def list_networks(self):
        if not self.networks:
            print("No networks are currently managed.")
            return

        print("Listing all managed networks:")
        for network in self.networks:
            print(f"Network Name: {network.network_name}")

    def connect_network_to_manager(self, network: DockerNetwork, container_manager: DockerContainerManager):
        print(f"Connecting container manager '{container_manager.get_container_manager_name()}' to network '{network.get_network_name()}'")

        containers = container_manager.get_containers()
        for container in containers:
            network.connect_container_to_network(container)


    def get_network(self, network_name: str) -> DockerNetwork:
        for network in self.networks:
            print(f"Network: {network}")
            if network.get_network_name == network_name:
                return network
        return None

if __name__ == "__main__":
    DNM = DockerNetworkManager("test_network_manager")
    DNM.create_networks()
    DNM.list_networks()
    DNM.remove_networks()
