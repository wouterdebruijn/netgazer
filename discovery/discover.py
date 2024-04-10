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
    params = {'ipv4': sys.argv[2]}

    print(f"Discovering {params['ipv4']}...")
    attributes = nmap_discover(params)

    print(attributes.__dict__)

    router = RouterSSH(params['ipv4'])

    # Get all device classes
    device_classes = RouterSSH.__subclasses__()

    matching_classes = list(
        filter(lambda device_class: device_class.vendor_match(attributes.vendor), device_classes))

    if len(matching_classes) == 0:
        print(f"Unsupported vendor {attributes.vendor}!")
        return

    router: RouterSSH = matching_classes[0](params['ipv4'])

    model = router.get_model()

    interfaces = router.get_interfaces()
    neighbors = router.get_arp_table()

    from netgazer.models import Device

    [device, _] = Device.objects.update_or_create(
        ipv4=params['ipv4'],
        name=f'{model} {params["ipv4"]}',
        manufacturer=attributes.vendor,
        model=model,
        os=attributes.os_name
    )

    # Update any neighbors that mention this device
    from netgazer.models import Neighbor

    neighbors = Neighbor.objects.filter(ipv4=params['ipv4'])

    for neighbor in neighbors:
        neighbor.neighbor_device = device
        neighbor.save()

    # Create interfaces
    from netgazer.models import Interface

    print(interfaces)

    for interface in interfaces:
        Interface.objects.update_or_create(
            device=device,
            name=interface['interface'],
            ipv4=interface['ip_address'],
        )

    for neighbor in neighbors:
        if neighbor['ip_address'] == device.ipv4:
            continue

        Neighbor.objects.update_or_create(
            device=device,
            ipv4=neighbor['ip_address'],
            name=f'unknown {neighbor["ip_address"]}',
        )

        # Run new discovery process for neighbor
        subprocess.call(
            ['python', 'netgazer_cli', 'discover', neighbor['ip_address']],
            stdout=subprocess.DE
        )


if __name__ == '__main__':
    discover()
