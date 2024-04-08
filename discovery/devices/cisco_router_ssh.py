from netmiko import ConnectHandler
from netmiko.base_connection import BaseConnection
from .generic import RouterSSH


class CiscoRouterSSH(RouterSSH):
    ipv4: str
    config: dict
    connection: BaseConnection

    @staticmethod
    def vendor_match(vendor: str) -> bool:
        return vendor.lower() == 'cisco'

    def __init__(self, ipv4, **kwargs):
        super().__init__(ipv4)

        self.config = {
            'device_type': 'cisco_ios',
            'host': ipv4,
            'username': 'cisco',
            'password': 'cisco',
            'ssh_config_file': '../ssh_config'
        }

        self.config.update(kwargs)
        self.connection = ConnectHandler(**self.config)

    def get_hostname(self):
        hostname = self.connection.send_command('show version')
        return hostname

    def get_interfaces(self):
        interfaces = self.connection.send_command('show ip interface brief')
        return interfaces

    def get_arp_table(self):
        arp_table = self.connection.send_command('show arp')
        return arp_table
