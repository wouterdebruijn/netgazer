import subprocess
import xml.etree.ElementTree as ET
from .devices import HuaweiRouterSSH, CiscoRouterSSH, RouterSSH
import sys


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
    device = {'ipv4': sys.argv[2]}

    print(f"Discovering {device['ipv4']}...")
    attributes = nmap_discover(device)

    print(attributes.__dict__)

    router = RouterSSH(device['ipv4'])

    # Get all device classes
    device_classes = RouterSSH.__subclasses__()

    matching_classes = list(
        filter(lambda device_class: device_class.vendor_match(attributes.vendor), device_classes))

    if len(matching_classes) == 0:
        print(f"Unsupported vendor {attributes.vendor}!")
        return

    router: RouterSSH = matching_classes[0](device['ipv4'])

    print(f"Hostname: {router.get_hostname()}")
    print(f"Interfaces: {router.get_interfaces()}")
    print(f"ARP Table: {router.get_arp_table()}")
    print(f"Discovered {device['ipv4']}!")

    from netgazer.models import Device

    device = Device.objects.create(
        ipv4=device['ipv4'],
        name=f'dummy {device["ipv4"]}',
    )


if __name__ == '__main__':
    discover()
