import docker 
import os
import json

class DockerContainerManager:
    def __init__(self, config_file): 
        try:
            with open(config_file, "r") as config_file:
                data = json.load(config_file)

                self.client = docker.from_env()
                self.image_name = data["image_name"]
                self.build_context = data["build_context"]
                self.container_name = data["container_name"]
                self.ports = data["ports"]
                self.network = data["networks"]
                self.container = None
        except FileNotFoundError:
            print(f"File not found: {config_file}")
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")


    def build_image(self):
        print(f"Building image '{self.image_name}'...")
        self.client.images.build(path=self.build_context, tag=self.image_name)

    def run_container(self):
        print(f"Running container '{self.container_name}'...")
        self.container = self.client.containers.run(
            self.image_name,
            detach=True,
            name=self.container_name,
            ports=self.ports,
            network=self.network
        )
    
    def stop_container(self):
        if self.container:
            print(f"Stopping container '{self.container_name}'...")
            self.container.stop()
        
    def remove_container(self):
        if self.container:
            print(f"Removing container '{self.container_name}'...")
            self.container.remove()

    @staticmethod
    def load_config(config_path):
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        
        with open(config_path, "r") as file:
            return json.load(file)