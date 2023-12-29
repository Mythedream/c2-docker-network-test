import logging
from modules.client_api import C2API

def setup_logging():
    logging.basicConfig(filename='app.log', 
                        filemode='a', 
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

def main():
    setup_logging()
    logging.info("Starting C2 Client")

    api = C2API()
    api.run()

if __name__ == "__main__":
    main()
