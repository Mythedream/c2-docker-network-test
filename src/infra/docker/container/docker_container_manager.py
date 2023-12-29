from docker_container import DockerContainer
from dataclasses import dataclass, field
import logging
from typing import Dict, Optional

@dataclass
class DockerContainerManager:
    containers: Dict[str, DockerContainer] = field(default_factory=dict)
    logger: logging.Logger = field(default=logging.getLogger("DockerContainerManager"))

    def add_container(self, container_name: str, docker_container: DockerContainer) -> bool:
        if container_name in self.containers:
            self.logger.warning(f"Container {container_name} already exists in the manager.")
            return False
        self.containers[container_name] = docker_container
        self.logger.info(f"Added container {container_name} to the manager.")
        return True

    def remove_container(self, container_name: str) -> bool:
        if container_name not in self.containers:
            self.logger.warning(f"Container {container_name} not found in the manager.")
            return False
        del self.containers[container_name]
        self.logger.info(f"Removed container {container_name} from the manager.")
        return True

    def get_container(self, container_name: str) -> Optional[DockerContainer]:
        return self.containers.get(container_name)

    def start_all_containers(self):
        for container_name, container in self.containers.items():
            container.start_container()
            self.logger.info(f"Started container {container_name}.")

    def stop_all_containers(self):
        for container_name, container in self.containers.items():
            container.stop_container()
            self.logger.info(f"Stopped container {container_name}.")