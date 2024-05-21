from typing import List
from netmiko import ConnectHandler
from netmiko.base_connection import BaseConnection
from .generic import Interface, RouterSSH, LldpNeighbor, ArpEntry
import logging

logger = logging.getLogger(__name__)


class HuaweiRouterSSH(RouterSSH):
    ipv4: str
    config: dict
    connection: BaseConnection

    @classmethod
    def vendor_match(cls, vendor: str) -> bool:
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

    def get_hostname(self) -> str:
        hostname = self.connection.send_command(
            'display current-configuration | include sysname', use_textfsm=True, textfsm_template='textfsm/huawei_display_current_config_sysname.textfsm')

        logger.debug(f'Hostname: {hostname}')

        return hostname[0]['sysname']

    def get_model(self) -> List[str]:
        version_info = self.connection.send_command(
            'display version', use_textfsm=True)

        logger.debug(f'Model: {version_info}')

        board_info = self.connection.send_command(
            'display elabel', use_textfsm=True, textfsm_template='textfsm/huawei_display_elabel.textfsm')

        logger.debug(f'Board Info: {board_info}')

        return [version_info[0]['model'], board_info[0]['serial']]

    def get_interfaces(self):
        interfaces = self.connection.send_command(
            'display ip interface brief', use_textfsm=True, textfsm_template='textfsm/huawei_display_ip_interface_brief.textfsm')

        mapped = []

        logger.debug(f'Interfaces: {interfaces}')

        for interface in interfaces:
            split_ip = interface['ip_address'].split(
                '/') if '/' in interface['ip_address'] else [interface['ip_address'], 24]

            mapped.append(Interface(
                name=interface['interface'],
                ipv4=split_ip[0] if split_ip[0] != 'unassigned' else None,
                ipv4_mask=split_ip[1] if split_ip[0] != 'unassigned' else None,
                physical=False if interface['physical'] == 'down' else True,
                protocol=False if interface['protocol'] == 'down' else True
            ))

        return mapped

    def get_arp_table(self):
        arp_table = self.connection.send_command(
            'display arp brief', use_textfsm=True)

        mapped = []

        logger.debug(f'ARP Table: {arp_table}')

        for entry in arp_table:
            mapped.append(ArpEntry(
                interface=entry['interface'],
                ipv4=entry['ip_address'],
                mac=entry['mac_address']
            ))

        return mapped

    def get_lldp_neighbors(self):
        lldp_neighbors = self.connection.send_command(
            'display lldp neighbor', use_textfsm=True, textfsm_template='textfsm/huawei_display_lldp_neighbor.textfsm')

        mapped = []

        logger.debug(f'LLDP neighbors: {lldp_neighbors}')

        for neighbor in lldp_neighbors:
            mapped.append(LldpNeighbor(
                interface=neighbor['interface'],
                mgmt_address=neighbor['managementaddress'],
                mgmt_address_type='mac' if 'all802' in neighbor['managementaddresstype'] else 'ipv4',
                system_name=neighbor['systemname']
            ))

        return mapped

    def get_license(self) -> str:
        license_info = self.connection.send_command(
            'display license', use_textfsm=True)

        logger.debug(f'License: {license_info}')

        return license_info
