from dataclasses import dataclass, field
import logging
from typing import Dict, Optional
from docker_volume import DockerVolume

@dataclass
class DockerVolumeManager:
    volumes: Dict[str, DockerVolume] = field(default_factory=dict)
    logger: logging.Logger = field(default=logging.getLogger("DockerVolumeManager"))

    def add_volume(self, volume_name: str, docker_volume: DockerVolume) -> bool:
        if volume_name in self.volumes:
            self.logger.warning(f"Volume {volume_name} already exists in the manager.")
            return False
        self.volumes[volume_name] = docker_volume
        self.logger.info(f"Added volume {volume_name} to the manager.")
        return True

    def remove_volume(self, volume_name: str) -> bool:
        if volume_name not in self.volumes:
            self.logger.warning(f"Volume {volume_name} not found in the manager.")
            return False
        if self.volumes[volume_name].is_in_use():
            self.logger.warning(f"Volume {volume_name} is currently in use and cannot be removed.")
            return False
        self.volumes[volume_name].remove()
        del self.volumes[volume_name]
        self.logger.info(f"Removed volume {volume_name} from the manager.")
        return True

    def get_volume(self, volume_name: str) -> Optional[DockerVolume]:
        return self.volumes.get(volume_name)

    def create_all_volumes(self):
        for volume_name, volume in self.volumes.items():
            volume.create()
            self.logger.info(f"Created volume {volume_name}.")

    def remove_all_volumes(self):
        for volume_name, volume in self.volumes.items():
            if not volume.is_in_use():
                volume.remove()
                self.logger.info(f"Removed volume {volume_name}.")
            else:
                self.logger.warning(f"Volume {volume_name} is currently in use and cannot be removed.")
