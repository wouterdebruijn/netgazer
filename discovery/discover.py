import subprocess
import uuid
import xml.etree.ElementTree as ET
from .devices import HuaweiRouterSSH, CiscoRouterSSH, RouterSSH
import sys
import logging

logger = logging.getLogger(__name__)


class NmapAttributes:
    type: str
    vendor: str
    os_family: str
    os_generation: str
    accuracy: str
    os_name: str


def nmap_discover(device):
    subprocess.call(
        ['sudo', 'nmap', device['ipv4'], '-p',
            '22,443,444', '-O', '-oX', 'nmap.xml'],
        stdout=subprocess.DEVNULL
    )

    tree = ET.parse('nmap.xml')

    root = tree.getroot()
    host = root.find('host')

    if host is None:
        logger.debug(f'Nmap output: {ET.tostring(root, encoding="unicode")}')
        logger.error(f'No host found for {device["ipv4"]}.')
        exit(1)

    os = host.find('os')
    osmatch = os.find('osmatch')

    if osmatch is None:
        return None

    osclass = osmatch.find('osclass')

    attributes = NmapAttributes()

    attributes.type = osclass.get('type')
    attributes.vendor = osclass.get('vendor')
    attributes.os_family = osclass.get('osfamily')
    attributes.os_generation = osclass.get('osgen')
    attributes.accuracy = osclass.get('accuracy')
    attributes.os_name = osmatch.get('name')

    return attributes


def discover():
    params = {'ipv4': sys.argv[2], 'run_id': sys.argv[3] if len(
        sys.argv) > 3 else uuid.uuid4()}

    logger.info(f"Discovering {params['ipv4']}...")

    # Initial nmap discovery to get vendor and OS
    attributes = nmap_discover(params)

    router: RouterSSH
    device_classes = RouterSSH.__subclasses__()
    matching_classes = list(
        filter(lambda device_class: device_class.vendor_match(attributes.vendor), device_classes))

    if len(matching_classes) == 0:
        logging.warn(
            f"No matching class found for device vendor {attributes.vendor}."
        )
        return

    # Select the first matching class, matched by device vendor
    router: RouterSSH = matching_classes[0](params['ipv4'])

    # Gather device information
    hostname = router.get_hostname()
    model = router.get_model()
    interfaces = router.get_interfaces()
    arp_entries = router.get_arp_table()
    lldp_neighbors = router.get_lldp_neighbors()

    from netgazer.models import Device

    # Gather a list of devices that were discovered in this run
    devices_in_run = Device.objects.filter(run_id=params['run_id'])

    if devices_in_run.filter(name=hostname).exists():
        logging.info(f"Device {hostname} already discovered.")
        return

    device, created = Device.objects.update_or_create(
        name=hostname,
        defaults={
            'os': attributes.os_name,
            'manufacturer': attributes.vendor,
            'model': model,
            'run_id': params['run_id'],
        }
    )

    if created:
        logging.info(f'\033[1;32mCreated\033[1;0m device {hostname}.')
    else:
        logging.info(f'\033[1;33mUpdated\033[1;0m device {hostname}.')

    # Update any neighbors that mention this device
    from netgazer.models import Neighbor

    me_neighbors = Neighbor.objects.filter(ipv4=params['ipv4'])

    for neighbor in me_neighbors:
        neighbor.neighbor_device = device
        neighbor.save()

    # Create interfaces
    from netgazer.models import Interface

    logger.debug(f"Interfaces: {interfaces}")

    for interface in interfaces:
        split_ip = interface['ip_address'].split(
            '/') if '/' in interface['ip_address'] else [interface['ip_address'], 24]

        _interface, created = Interface.objects.update_or_create(
            device=device,
            name=interface['interface'],
            defaults={
                'ipv4': split_ip[0],
                'ipv4_mask': split_ip[1],
            }
        )

        if created:
            logging.info(f'\033[1;32mCreated\033[1;0m interface {_interface}.')
        else:
            logging.info(f'\033[1;33mUpdated\033[1;0m interface {_interface}.')

    my_addresses = device.interface_set.values_list('ipv4', flat=True)

    logger.debug(f"ARP entries: {arp_entries}")

    for arp_entry in arp_entries:
        if arp_entry['ip_address'] in my_addresses:
            continue

        # Create or update neighbor entries for the current device
        neighbor, created = Neighbor.objects.update_or_create(
            device=device,
            ipv4=arp_entry['ip_address'],
            defaults={
                'name': f"{arp_entry['ip_address']} ({arp_entry['mac_address']})",
            },
        )

        if created:
            logging.info(
                f'\033[1;32mCreated\033[1;0m neighbor {neighbor}.')
        else:
            logging.info(
                f'\033[1;33mUpdated\033[1;0m neighbor {neighbor}.')

        # Check if the neighbor is known
        known_neighbor = devices_in_run.filter(
            interface__ipv4=arp_entry['ip_address'])
        if known_neighbor.exists():
            neighbor.neighbor_device = known_neighbor.first()
            neighbor.save()
            continue

        # Run new discovery process for neighbor
        subprocess.call(
            ['python', 'netgazer_cli.py', 'discover',
                arp_entry['ip_address'], str(params['run_id'])]
        )


if __name__ == '__main__':
    discover()
