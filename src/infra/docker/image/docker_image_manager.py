from dataclasses import dataclass, field
import logging
import json
from typing import Optional, Dict, List
from docker_image import DockerImage

@dataclass
class DockerImageManager:
    images: Dict[str, DockerImage] = field(default_factory=dict)
    logger: logging.Logger = field(default=logging.getLogger("DockerImageManager"))
    default_registry: str = ""

    def add_image(self, docker_image: DockerImage) -> bool:
        if docker_image.get_image_name() in self.images:
            self.logger.warning(f"Image {docker_image.get_image_name()} already exists in the manager.")
            return False
        self.images[docker_image.get_image_name()] = docker_image
        self.logger.info(f"Added Docker image {docker_image.get_image_name()} to the manager.")
        return True

    def remove_image(self, image_name: str) -> bool:
        if image_name not in self.images:
            self.logger.warning(f"Image {image_name} not found in the manager.")
            return False
        del self.images[image_name]
        self.logger.info(f"Removed Docker image {image_name} from the manager.")
        return True

    def get_image(self, image_name: str) -> Optional[DockerImage]:
        return self.images.get(image_name)

    def pull_all_images(self) -> Dict[str, bool]:
        results = {}
        for image_name, image in self.images.items():
            result = image.pull_image()
            results[image_name] = result is not None
        return results

    def build_all_images(self) -> Dict[str, bool]:
        results = {}
        for image_name, image in self.images.items():
            if image.get_build_path():
                result = image.build_image()
                results[image_name] = result is not None
        return results

    def push_all_images(self, registry: Optional[str] = None) -> Dict[str, bool]:
        results = {}
        registry = registry or self.default_registry
        for image_name, image in self.images.items():
            if image.get_state()['tagged']:
                result = image.push_image(registry)
                results[image_name] = result
        return results

    def list_all_images(self) -> List[str]:
        return list(self.images.keys())

    def save_state(self, file_path: str) -> bool:
        try:
            with open(file_path, 'w') as file:
                json.dump(list(self.images.keys()), file)
            self.logger.info("State saved successfully.")
            return True
        except Exception as e:
            self.logger.error(f"Error saving state: {e}")
            return False

    def load_state(self, file_path: str) -> bool:
        try:
            with open(file_path, 'r') as file:
                image_names = json.load(file)
            for name in image_names:
                self.add_image(DockerImage(name))
            self.logger.info("State loaded successfully.")
            return True
        except Exception as e:
            self.logger.error(f"Error loading state: {e}")
            return False

    def set_default_registry(self, registry: str):
        self.default_registry = registry
