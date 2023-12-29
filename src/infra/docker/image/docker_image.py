from dataclasses import dataclass, field
import docker
import logging

@dataclass
class DockerImage:
    _image_name: str
    _build_path: str = None
    _build_tag: str = None
    logger: logging.Logger = field(default=logging.getLogger("DockerImage"))
    _image_info: dict = field(default_factory=dict, init=False)
    _state: dict = field(default_factory=lambda: {'pulled': False, 'built': False, 'tagged': False}, init=False)

    def __post_init__(self):
        self.client = docker.from_env()

    def get_image_name(self):
        return self._image_name

    def set_image_name(self, image_name):
        self._image_name = image_name

    def get_build_path(self):
        return self._build_path

    def set_build_path(self, build_path):
        self._build_path = build_path

    def get_build_tag(self):
        return self._build_tag

    def set_build_tag(self, build_tag):
        self._build_tag = build_tag

    def get_image_info(self):
        return self._image_info

    def get_state(self):
        return self._state

    def pull_image(self):
        try:
            self.logger.info(f"Pulling image {self.get_image_name()}...")
            image = self.client.images.pull(self.get_image_name())
            self._image_info = image.attrs
            self._state['pulled'] = True
            self.logger.info("Image pulled successfully.")
            return image
        except docker.errors.APIError as e:
            self.logger.error(f"Failed to pull image {self.get_image_name()}: {e}")
            return None

    def build_image(self):
        if not self.get_build_path():
            self.logger.warning(f"No build path specified for image {self.get_image_name()}")
            return None
        try:
            tag = self.get_build_tag() or self.get_image_name()
            self.logger.info(f"Building image {tag} from {self.get_build_path()}...")
            image, _ = self.client.images.build(path=self.get_build_path(), tag=tag)
            self._image_info = image.attrs
            self._state['built'] = True
            self.logger.info("Image built successfully.")
            return image
        except docker.errors.BuildError as e:
            self.logger.error(f"Failed to build image {tag}: {e}")
            return None
        except docker.errors.APIError as e:
            self.logger.error(f"API error occurred while building image: {e}")
            return None

    def tag_image(self, new_tag: str):
        if not self.get_state()['pulled'] and not self.get_state()['built']:
            self.logger.warning(f"Image {self.get_image_name()} has not been pulled or built yet.")
            return False
        try:
            self.logger.info(f"Tagging image {self.get_image_name()} with {new_tag}...")
            image = self.client.images.get(self.get_image_name())
            image.tag(new_tag)
            self._state['tagged'] = True
            self.logger.info("Image tagged successfully.")
            return True
        except docker.errors.ImageNotFound as e:
            self.logger.error(f"Image {self.get_image_name()} not found: {e}")
            return False
        except docker.errors.APIError as e:
            self.logger.error(f"API error occurred while tagging image: {e}")
            return False

    def push_image(self, registry: str):
        if not self.get_state()['tagged']:
            self.logger.warning(f"Image {self.get_image_name()} has not been tagged yet.")
            return False
        try:
            self.logger.info(f"Pushing image {self.get_image_name()} to registry {registry}...")
            response = self.client.images.push(self.get_image_name(), stream=True, decode=True)
            for line in response:
                self.logger.info(line)
            self.logger.info("Image pushed successfully.")
            return True
        except docker.errors.APIError as e:
            self.logger.error(f"Failed to push image {self.get_image_name()}: {e}")
            return False

    def remove_image(self, force: bool = False):
        try:
            self.logger.info(f"Removing image {self.get_image_name()}...")
            self.client.images.remove(self.get_image_name(), force=force)
            self._state = {'pulled': False, 'built': False, 'tagged': False}
            self.logger.info("Image removed successfully.")
            return True
        except docker.errors.ImageNotFound as e:
            self.logger.error(f"Image {self.get_image_name()} not found: {e}")
            return False
        except docker.errors.APIError as e:
            self.logger.error(f"API error occurred while removing image: {e}")
            return False

    def list_tags(self):
        try:
            image = self.client.images.get(self.get_image_name())
            return image.tags
        except docker.errors.ImageNotFound as e:
            self.logger.error(f"Image {self.get_image_name()} not found: {e}")
            return []

    def inspect_image(self):
        try:
            image = self.client.images.get(self.get_image_name())
            return image.attrs
        except docker.errors.ImageNotFound as e:
            self.logger.error(f"Image {self.get_image_name()} not found: {e}")
            return None

