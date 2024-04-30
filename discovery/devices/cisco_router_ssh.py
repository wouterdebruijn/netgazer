from netmiko import ConnectHandler
from netmiko.base_connection import BaseConnection
from .generic import RouterSSH, Interface


class CiscoRouterSSH(RouterSSH):
    ipv4: str
    config: dict
    connection: BaseConnection

    @classmethod
    def vendor_match(cls, vendor: str) -> bool:
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

    def get_model(self):
        hostname = self.connection.send_command('show version')
        return hostname

    def get_interfaces(self):
        interfaces = self.connection.send_command('show ip interface brief')

        mapped = []

        for interface in interfaces:
            mapped.append(Interface(
                name=interface['interface'],
                ipv4=interface['ip_address'] if interface['ip_address'] != 'unassigned' else None,
                physical=interface['physical'],
                protocol=interface['protocol']
            ))

        return mapped

    def get_arp_table(self):
        arp_table = self.connection.send_command('show arp')

        mapped = []

        for entry in arp_table:
            mapped.append(Neighbor(
                name=entry['mac_address'],
                ipv4=entry['ip_address'],
                interface_name=entry['interface']
            ))

        return mapped

    def get_lldp_neighbors(self):
        lldp_table = self.connection.send_command('show lldp neighbors')

        mapped = []

        for entry in lldp_table:
            mapped.append(Neighbor(
                name=entry['neighbor'],
                ipv4=None,
                interface_name=entry['local_interface']
            ))

        return mapped
