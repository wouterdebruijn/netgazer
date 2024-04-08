from netmiko import ConnectHandler
from netmiko.base_connection import BaseConnection
from .generic import RouterSSH


class HuaweiRouterSSH(RouterSSH):
    ipv4: str
    config: dict
    connection: BaseConnection

    @staticmethod
    def vendor_match(vendor: str) -> bool:
        return vendor.lower() == 'huawei'

    def __init__(self, ipv4, **kwargs):
        super().__init__(ipv4)

        self.config = {
            'device_type': 'huawei',
            'host': ipv4,
            'username': 'admin',
            'password': 'Admin@huawei',
            'ssh_config_file': '../ssh_config'
        }

        self.config.update(kwargs)
        self.connection = ConnectHandler(**self.config)

    def get_hostname(self):
        hostname = self.connection.send_command('display version')
        return hostname

    def get_interfaces(self):
        interfaces = self.connection.send_command('display ip interface')
        return interfaces

    def get_arp_table(self):
        arp_table = self.connection.send_command('display arp')
        return arp_table
