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
            'device_type': 'huawei_vrp',
            'host': ipv4,
            'username': 'admin',
            'password': 'Admin@huawei',
            'ssh_config_file': '../ssh_config'
        }

        self.config.update(kwargs)
        self.connection = ConnectHandler(**self.config)

    def get_model(self):
        version_info = self.connection.send_command(
            'display version', use_textfsm=True)

        return version_info[0]['model']

    def get_interfaces(self):
        interfaces = self.connection.send_command(
            'display ip interface brief', use_textfsm=True, textfsm_template='textfsm/huawei_display_ip_interface_brief.textfsm')
        return interfaces

    def get_arp_table(self):
        arp_table = self.connection.send_command(
            'display arp brief', use_textfsm=True)
        return arp_table
