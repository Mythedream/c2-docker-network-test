import psutil
import dataclasses
import socket
import logging

from log_config import setup_logging

# Initialize logging
setup_logging()
logger = logging.getLogger(__name__)

@dataclasses.dataclass
class NetworkStatistics:
    bytes_sent: int = None
    bytes_received: int = None
    packets_sent: int = None
    packets_received: int = None
    active_interfaces: dict = None

    def gather_network_stats(self):
        logger.info("Starting to gather network statistics")
        try:
            self._set_bytes_sent()
            self._set_bytes_received()
            self._set_packets_sent()
            self._set_packets_received()
            self._set_active_interfaces()
        except Exception as e:
            logger.error(f"Error gathering network stats: {e}")
        else:
            logger.info("Successfully gathered network statistics")

    def _set_bytes_sent(self):
        net_io = psutil.net_io_counters()
        self.bytes_sent = net_io.bytes_sent
        logger.info(f"Bytes sent: {self.bytes_sent}")

    def _set_bytes_received(self):
        net_io = psutil.net_io_counters()
        self.bytes_received = net_io.bytes_recv
        logger.info(f"Bytes received: {self.bytes_received}")

    def _set_packets_sent(self):
        net_io = psutil.net_io_counters()
        self.packets_sent = net_io.packets_sent
        logger.info(f"Packets sent: {self.packets_sent}")

    def _set_packets_received(self):
        net_io = psutil.net_io_counters()
        self.packets_received = net_io.packets_recv
        logger.info(f"Packets received: {self.packets_received}")

    def _set_active_interfaces(self):
        interfaces = psutil.net_if_addrs()
        formatted_interfaces = {}
        for interface_name, addresses in interfaces.items():
            formatted_addresses = []
            for addr in addresses:
                if addr.family == socket.AF_INET or addr.family == socket.AF_INET6:
                    formatted_addresses.append(f"{addr.address} (netmask: {addr.netmask})")
            formatted_interfaces[interface_name] = formatted_addresses
        self.active_interfaces = formatted_interfaces
        logger.info(f"Active interfaces: {self.active_interfaces}")

    def _format_bytes(self, size):
        # Simple formatter for bytes to a more readable format
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024:
                return f"{size:.2f}{unit}"
            size /= 1024
        return f"{size:.2f}TB"

    def __str__(self):
        self.gather_network_stats()
        formatted_output = []

        for key, value in dataclasses.asdict(self).items():
            if key in ["bytes_sent", "bytes_received"]:
                value = self._format_bytes(value)
            if key != "active_interfaces":
                formatted_output.append(f"{key.ljust(20)}: {value}")
            else:
                formatted_output.append("active_interfaces:".ljust(20))
                for intf_name, intf_addresses in value.items():
                    formatted_output.append(f"  {intf_name.ljust(18)}: {', '.join(intf_addresses)}")

        return '\n'.join(formatted_output)

# Example usage
if __name__ == "__main__":
    net_stats = NetworkStatistics()
    print(net_stats)
