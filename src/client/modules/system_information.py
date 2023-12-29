import requests
import socket
import uuid
import platform
import netifaces
import dataclasses
import logging

from log_config import setup_logging

# Initialize logging
setup_logging()
logger = logging.getLogger(__name__)

@dataclasses.dataclass
class SystemInformation:
    hostname: str = None
    internal_ip: str = None
    external_ip: str = None
    mac_address: str = None
    platform: str = None
    platform_release: str = None
    geo_info: dict = None

    def gather_information(self):
        logger.info("Starting to gather system information")
        self.hostname = self._set_hostname()
        self.internal_ip = self._set_internal_ip_address()
        self.external_ip = self._set_external_ip_address()
        self.mac_address = self._set_mac_address()
        self.platform = self._set_platform()
        self.platform_release = self._set_platform_release()
        self.geo_info = self._set_geolocation_info()
        logger.info("System information gathered successfully")

    def _set_hostname(self):
        hostname = socket.gethostname()
        logger.info(f"Hostname: {hostname}")
        return hostname
    
    def _set_platform(self):
        platform_name = platform.system()
        logger.info(f"Platform: {platform_name}")
        return platform_name
    
    def _set_platform_release(self):
        platform_release = platform.release()
        logger.info(f"Platform Release: {platform_release}")
        return platform_release
    
    def _set_mac_address(self):
        try:
            gws = netifaces.gateways()
            interface = gws['default'][netifaces.AF_INET][1]
            mac = netifaces.ifaddresses(interface)[netifaces.AF_LINK][0]["addr"]
            logger.info(f"MAC Address: {mac}")
            return mac
        except Exception as e:
            logger.error(f"Unable to determine MAC: {e}")
            return "Unable to determine MAC"

    def _set_internal_ip_address(self):
        try:
            gws = netifaces.gateways()
            interface = gws['default'][netifaces.AF_INET][1]
            ip = netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['addr']
            logger.info(f"Internal IP Address: {ip}")
            return ip
        except Exception as e:
            logger.error(f"Unable to determine IP: {e}")
            return "Unable to determine IP"

    def _set_external_ip_address(self):
        try:
            response = requests.get("https://api.ipify.org")
            if response.status_code == 200:
                external_ip = response.text
                logger.info(f"External IP Address: {external_ip}")
                return external_ip
            else:
                logger.error("Unable to determine external IP")
                return "Unable to determine external IP"
        except requests.RequestException as e:
            logger.error(f"Request failed: {e}")
            return "Request failed"

    def _set_geolocation_info(self):
        if self.external_ip:
            try:
                response = requests.get(f"https://ipinfo.io/{self.external_ip}/json")
                if response.status_code == 200:
                    geo_info = response.json()
                    logger.info(f"Geolocation Info: {geo_info}")
                    return geo_info
                else:
                    logger.error("Unable to determine geolocation")
                    return "Unable to determine geolocation"
            except requests.RequestException as e:
                logger.error(f"Request failed: {e}")
                return "Request failed"

    def __str__(self):
        self.gather_information()  # Ensure information is gathered before printing
        class_vars = vars(self)
        return '\n'.join(f"{key}: {value}" for key, value in class_vars.items())

# Example usage
if __name__ == "__main__":
    system_info = SystemInformation()
    print(system_info)
