from docker_network_manager import DockerNetworkManager
from docker_container_manager import DockerContainerManager

class DockerOrchestrator:
    def __init__(self, orchestrator_name = "c2-orchestrator", network_manager_name = "c2-network-manager", container_manager_name = "c2-container-manager"):
        self.name = orchestrator_name
        self.network_manager = DockerNetworkManager(name=network_manager_name)
        self.container_manager = DockerContainerManager(name=container_manager_name)

    def start_infrastructure(self):
        print("Starting infrastructure")
        self.network_manager.create_networks()
        self.container_manager.start_containers()

        self.connect_infrastructure()
        

    def connect_infrastructure(self):
        print("Connecting infrastructure")
        self.network_manager.connect_network_to_manager(self.network_manager.get_network("c2-network"), self.container_manager)


    def stop_infrastructure(self):
        print("Stopping infrastructure")
        self.container_manager.shutdown_containers()
        self.network_manager.remove_networks()


if __name__ == "__main__":
    DO = DockerOrchestrator()
    DO.stop_infrastructure()
    DO.start_infrastructure()
