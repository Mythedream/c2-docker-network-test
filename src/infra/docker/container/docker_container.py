from dataclasses import dataclass, field
from typing import Dict, Optional
import docker
import logging

from src.infra.docker.image.docker_image import DockerImage


# TODO integrate docker volume
@dataclass
class DockerContainer:
    container_image: DockerImage
    client: docker.DockerClient = field(default_factory=docker.from_env)
    logger: logging.Logger = field(default=logging.getLogger("DockerContainer"))
    container_id: str = field(init=False, default=None)

    def create_container(self, command=None, environment=None, volumes=None, ports=None):
        try:
            self.logger.info(f"Creating container from image {self.container_image.get_image_name()}...")
            container = self.client.containers.create(
                self.container_image.get_image_name(),
                command=command,
                environment=environment,
                volumes=volumes,
                ports=ports
            )
            self.container_id = container.id
            self.logger.info(f"Container {self.container_id} created.")
            return True
        except docker.errors.ImageNotFound as e:
            self.logger.error(f"Image not found: {e}")
            return False
        except docker.errors.APIError as e:
            self.logger.error(f"API error: {e}")
            return False

    def start_container(self):
        if self.container_id:
            try:
                self.logger.info(f"Starting container {self.container_id}...")
                container = self.client.containers.get(self.container_id)
                container.start()
                self.logger.info("Container started.")
                return True
            except docker.errors.APIError as e:
                self.logger.error(f"API error: {e}")
                return False
        else:
            self.logger.warning("No container created to start.")
            return False

    def stop_container(self):
        if self.container_id:
            try:
                self.logger.info(f"Stopping container {self.container_id}...")
                container = self.client.containers.get(self.container_id)
                container.stop()
                self.logger.info("Container stopped.")
                return True
            except docker.errors.APIError as e:
                self.logger.error(f"API error: {e}")
                return False
        else:
            self.logger.warning("No container created to stop.")
            return False

    def remove_container(self, force=False):
        if self.container_id:
            try:
                self.logger.info(f"Removing container {self.container_id}...")
                container = self.client.containers.get(self.container_id)
                container.remove(force=force)
                self.logger.info("Container removed.")
                self.container_id = None
                return True
            except docker.errors.APIError as e:
                self.logger.error(f"API error: {e}")
                return False
        else:
            self.logger.warning("No container created to remove.")
            return False

    def inspect_container(self):
        if self.container_id:
            try:
                container = self.client.containers.get(self.container_id)
                return container.attrs
            except docker.errors.NotFound:
                self.logger.error("Container not found.")
            except docker.errors.APIError as e:
                self.logger.error(f"API error: {e}")
        else:
            self.logger.warning("No container created to inspect.")
        return None

    def get_logs(self):
        if self.container_id:
            try:
                container = self.client.containers.get(self.container_id)
                return container.logs()
            except docker.errors.NotFound:
                self.logger.error("Container not found.")
            except docker.errors.APIError as e:
                self.logger.error(f"API error: {e}")
        else:
            self.logger.warning("No container created to get logs from.")
        return None

    def execute_command(self, command):
        if self.container_id:
            try:
                container = self.client.containers.get(self.container_id)
                exit_code, output = container.exec_run(command)
                return exit_code, output
            except docker.errors.NotFound:
                self.logger.error("Container not found.")
            except docker.errors.APIError as e:
                self.logger.error(f"API error: {e}")
        else:
            self.logger.warning("No container created to execute command.")
        return None, None

    def restart_container(self):
        if self.container_id:
            try:
                container = self.client.containers.get(self.container_id)
                container.restart()
                self.logger.info("Container restarted.")
                return True
            except docker.errors.NotFound:
                self.logger.error("Container not found.")
            except docker.errors.APIError as e:
                self.logger.error(f"API error: {e}")
        else:
            self.logger.warning("No container created to restart.")
        return False

    def pause_container(self):
        if self.container_id:
            try:
                container = self.client.containers.get(self.container_id)
                container.pause()
                self.logger.info("Container paused.")
                return True
            except docker.errors.NotFound:
                self.logger.error("Container not found.")
            except docker.errors.APIError as e:
                self.logger.error(f"API error: {e}")
        else:
            self.logger.warning("No container created to pause.")
        return False

    def unpause_container(self):
        if self.container_id:
            try:
                container = self.client.containers.get(self.container_id)
                container.unpause()
                self.logger.info("Container unpaused.")
                return True
            except docker.errors.NotFound:
                self.logger.error("Container not found.")
            except docker.errors.APIError as e:
                self.logger.error(f"API error: {e}")
        else:
            self.logger.warning("No container created to unpause.")
        return False

    def get_resource_usage(self):
        if self.container_id:
            try:
                container = self.client.containers.get(self.container_id)
                return container.stats(stream=False)
            except docker.errors.NotFound:
                self.logger.error("Container not found.")
            except docker.errors.APIError as e:
                self.logger.error(f"API error: {e}")
        else:
            self.logger.warning("No container created to get resource usage.")
        return None
    
    def start_all_containers(self):
        for container_name, container in self.containers.items():
            container.start_container()
            self.logger.info(f"Started container {container_name}.")

    def stop_all_containers(self):
        for container_name, container in self.containers.items():
            container.stop_container()
            self.logger.info(f"Stopped container {container_name}.")

    def restart_all_containers(self):
        for container_name, container in self.containers.items():
            container.restart_container()
            self.logger.info(f"Restarted container {container_name}.")

    def pause_all_containers(self):
        for container_name, container in self.containers.items():
            container.pause_container()
            self.logger.info(f"Paused container {container_name}.")

    def unpause_all_containers(self):
        for container_name, container in self.containers.items():
            container.unpause_container()
            self.logger.info(f"Unpaused container {container_name}.")

    def get_all_container_logs(self):
        logs = {}
        for container_name, container in self.containers.items():
            logs[container_name] = container.get_logs()
        return logs

    def execute_command_in_all_containers(self, command):
        results = {}
        for container_name, container in self.containers.items():
            exit_code, output = container.execute_command(command)
            results[container_name] = (exit_code, output)
        return results

    def inspect_all_containers(self):
        info = {}
        for container_name, container in self.containers.items():
            info[container_name] = container.inspect_container()
        return info

    def get_all_container_resource_usage(self):
        usage = {}
        for container_name, container in self.containers.items():
            usage[container_name] = container.get_resource_usage()
        return usage