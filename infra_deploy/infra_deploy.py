from container_manager.container_manager import DockerContainerManager
from network_manager.network_manager import DockerNetworkManager

def main():
    try: 
        server_config = "infra_deploy/container_manager/server_config.json"
        client_config = "infra_deploy/container_manager/client_config.json"

        # Network management
        print("Setting up docker network...")
        config_file = "infra_deploy/network_manager/network_config.json"
        network_manager = DockerNetworkManager(config_file)
        network_manager.create_network()
        print("Finished setting up docker network.")

        # Server container management 
        print("Setting up C2 server...")
        server_manager = DockerContainerManager(server_config)
        server_manager.build_image()
        server_manager.run_container()
        print("Finished setting up C2 server...")

        # Client container management
        print("Setting up C2 client...")
        client_manager = DockerContainerManager(client_config)
        client_manager.build_image()
        client_manager.run_container()
        print("Finished setting up C2 client.")

    except FileNotFoundError as e:
        print(e)
        return

if __name__ == "__main__":
    main()