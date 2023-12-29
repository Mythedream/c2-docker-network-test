from dataclasses import dataclass, field
import docker
import logging

@dataclass
class DockerVolume:
    client: docker.DockerClient = field(default_factory=docker.from_env)
    logger: logging.Logger = field(default=logging.getLogger("DockerVolume"))
    volume_name: str
    volume_id: str = field(init=False, default=None)

    def create(self, driver: str = "local", driver_opts: dict = None, labels: dict = None):
        try:
            self.logger.info(f"Creating volume '{self.volume_name}' with driver '{driver}'...")
            volume = self.client.volumes.create(
                name=self.volume_name, 
                driver=driver, 
                driver_opts=driver_opts, 
                labels=labels
            )
            self.volume_id = volume.id
            self.logger.info(f"Volume '{self.volume_name}' created.")
            return True
        except docker.errors.APIError as e:
            self.logger.error(f"API error: {e}")
            return False

    def inspect(self):
        if self.volume_id:
            try:
                volume = self.client.volumes.get(self.volume_id)
                return volume.attrs
            except docker.errors.NotFound:
                self.logger.error("Volume not found.")
            except docker.errors.APIError as e:
                self.logger.error(f"API error: {e}")
        else:
            self.logger.warning("Volume has not been created yet.")
        return None

    def is_in_use(self):
        if self.volume_id:
            try:
                volume = self.client.volumes.get(self.volume_id)
                return 'Containers' in volume.attrs and len(volume.attrs['Containers']) > 0
            except docker.errors.NotFound:
                self.logger.error("Volume not found.")
            except docker.errors.APIError as e:
                self.logger.error(f"API error: {e}")
            return False
        else:
            self.logger.warning("Volume has not been created yet.")
            return False

    def remove(self):
        if self.volume_id:
            try:
                volume = self.client.volumes.get(self.volume_id)
                volume.remove()
                self.logger.info(f"Volume '{self.volume_name}' removed.")
                self.volume_id = None
                return True
            except docker.errors.NotFound:
                self.logger.error("Volume not found.")
            except docker.errors.APIError as e:
                self.logger.error(f"API error: {e}")
        else:
            self.logger.warning("Volume has not been created yet.")
        return False