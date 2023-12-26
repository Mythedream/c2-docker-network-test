import docker
import json

class DockerNetworkManager:
    def __init__(self, config_file):
        try:
            with open(config_file, "r") as config_file:
                data = json.load(config_file)
                self.client = docker.from_env()
                self.network_name = data["name"]
                self.driver = data["driver"]
                self.network = None
        except FileNotFoundError:
            print(f"File not found: {config_file}")
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")

    def create_network(self):
        try:
            print(f"Creating network '{self.network_name}' with driver '{self.driver}'")
            self.network = self.client.networks.create(self.network_name, driver=self.driver)
            print(f"Network '{self.network_name}' created")
        except Exception as e:
            print(f"Error creating network: {e}")

    def remove_network(self):
        if self.network:
            try:
                print(f"Removing network '{self.network_name}'")
                self.network.remove()
                print(f"Network '{self.network_name}' removed")
            except Exception as e:
                print(f"Error removing network: {e}")

if __name__ == "__main__":
    config_file = "infra_deploy/network_manager/network_config.json"
    network_manager = DockerNetworkManager(config_file)
    network_manager.create_network()