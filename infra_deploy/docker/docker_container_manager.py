import json
import os
import glob

from docker_container import DockerContainer

class DockerContainerManager:
    def __init__(self, name: str):
        self.name = name
        self.containers = []

    def _is_valid_json_config(self, json_config_path):
        return os.path.exists(json_config_path)

    def add_container(self, container: DockerContainer):
        print(f"Appending container '{container.get_container_name()}' to list...")
        self.containers.append(container)

    def start_container(self, json_config_path):
        if not self._is_valid_json_config(json_config_path):
            raise ValueError("Invalid JSON configuration.")
    
        with open(json_config_path, "r") as json_file:
            data = json.load(json_file)

        existing_container = self.get_container(data["container_name"])
        if existing_container:
            print(f"Container {data['container_name']} already exists, Removing it.")
            existing_container.stop_container()
            existing_container.remove_container()

        container = DockerContainer(
            image_name=data["image_name"],
            container_name=data["container_name"],
            ports=data["open_ports"],
            volumes=data["volumes"] 
        )

        container.build_container()
        container.run_container()
        self.add_container(container)

    def start_containers(self, config_directory="./container_configs"):
        # Construct the full path to the configuration directory
        base_path = os.path.dirname(__file__)
        full_config_path = os.path.join(base_path, config_directory)

        # List all JSON files in the directory
        config_files = glob.glob(os.path.join(full_config_path, "*.json"))

        for config_file in config_files:
            try:
                self.start_container(config_file)
                print(f"Container started from {config_file}")
            except Exception as e:
                print(f"Failed to start container from {config_file}: {e}")

    def shut_down_container(self, container: DockerContainer):
        print(f"Stopping container: {container.get_container_name()}")
        container.stop_container()
        container.remove_container()

    def shutdown_containers(self):
        for container in self.containers:
            self.shut_down_container(container)

    def list_containers(self):
        if not self.containers:
            print("No containers are currently managed.")
            return
        
        print("Listing all managed containers:")
        for container in self.containers:
            print(f"Container Name: {container.get_container_name()}")

    def get_container_manager_name(self) -> str:
        return self.name

    def get_container(self, container_name: str) -> DockerContainer:
        for container in self.containers:
            if container.get_container_name() == container_name:
                return container
        return None

    def get_containers(self) -> []:
        return self.containers

if __name__ == "__main__":
    DCM = DockerContainerManager("test_manager")
    DCM.start_containers()
    DCM.list_containers()
    DCM.shutdown_containers()
