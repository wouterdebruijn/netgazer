from typing import List
from netmiko import ConnectHandler
from netmiko.base_connection import BaseConnection
from .generic import Interface, RouterSSH, LldpNeighbor, ArpEntry
import logging

logger = logging.getLogger(__name__)


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

        self.connection.send_command('enable', expect_string='#$')

    def get_hostname(self) -> str:
        hostname = self.connection.send_command(
            'show run | i hostname', use_textfsm=True, textfsm_template='textfsm/cisco_show_running_config_sysname.textfsm')

        logging.debug(f'Hostname: {hostname}')

        return hostname[0]['hostname']

    def get_model(self) -> List[str]:
        version_info = self.connection.send_command(
            'show version', use_textfsm=True)

        logging.debug(f'Model: {version_info}')

        return [version_info[0]['hardware'][0], version_info[0]['serial'][0]]

    def get_interfaces(self):
        interfaces = self.connection.send_command(
            'show ip interface', use_textfsm=True)

        mapped = []

        logging.debug(f'Interfaces: {interfaces}')

        for interface in interfaces:
            mapped.append(Interface(
                name=interface['interface'],
                ipv4=interface['ip_address'][0] if len(
                    interface['ip_address']) > 0 else None,
                ipv4_mask=interface['prefix_length'][0] if len(
                    interface['prefix_length']) > 0 else None,
                physical=interface['link_status'],
                protocol=interface['protocol_status']
            ))

        return mapped

    def get_arp_table(self):
        arp_table = self.connection.send_command(
            'show ip arp', use_textfsm=True)

        mapped = []

        logging.debug(f'ARP Table: {arp_table}')

        for entry in arp_table:
            mapped.append(ArpEntry(
                interface=entry['interface'],
                ipv4=entry['ip_address'],
                mac=entry['mac_address']
            ))

        return mapped

    def get_lldp_neighbors(self):
        lldp_neighbors = self.connection.send_command(
            'show lldp neighbors detail', use_textfsm=True)

        mapped = []

        logging.debug(f'LLDP Neighbors: {lldp_neighbors}')

        for neighbor in lldp_neighbors:
            mapped.append(LldpNeighbor(
                interface=neighbor['local_interface'],
                mgmt_address=neighbor['management_ip'] if neighbor['management_ip'] != '' else neighbor['chassis_id'],
                mgmt_address_type='mac' if neighbor['management_ip'] == '' else 'ipv4',
                system_name=neighbor['neighbor']
            ))

        return mapped

    def get_license(self):
        try:
            license_info = self.connection.send_command(
                'show license', use_textfsm=True)

        except Exception as e:
            logging.error(
                f"An error occurred while fetching license information: {e}")
            license_info = ''

        logging.debug(f'License: {license_info}')

        return license_info
