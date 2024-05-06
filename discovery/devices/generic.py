from abc import ABC, abstractmethod
from typing import List


class Interface():
    name: str
    ipv4: str | None
    ipv4_mask: int | None
    physical: str
    protocol: str

    def __init__(self, name, ipv4, ipv4_mask, physical, protocol):
        self.name = name
        self.ipv4 = ipv4
        self.ipv4_mask = ipv4_mask
        self.physical = physical
        self.protocol = protocol


class ArpEntry():
    ipv4: str
    mac: str
    interface: str

    def __init__(self, ipv4, mac, interface):
        self.ipv4 = ipv4
        self.mac = mac
        self.interface = interface


class LldpNeighbor():
    mgmt_address: str
    mgmt_address_type: str
    system_name: str
    interface: str

    def __init__(self, mgmt_address, mgmt_address_type, system_name, interface):
        self.mgmt_address = mgmt_address
        self.mgmt_address_type = mgmt_address_type
        self.system_name = system_name
        self.interface = interface


class RouterSSH(ABC):
    ipv4: str

    def __init__(self, ipv4):
        self.ipv4 = ipv4

    @classmethod
    @abstractmethod
    def vendor_match(cls, vendor: str) -> bool:
        """
        Check if the vendor matches the current device
        """
        print(f"vendor_match is implemented on {cls.__class__.__name__}")

    @abstractmethod
    def get_hostname(self) -> str:
        """
        Get the hostname of the device, e.g. 'router1'
        """
        print(f"get_hostname is implemented on {self.__class__.__name__}")

    @abstractmethod
    def get_model(self) -> List[str]:
        """
        Get the model of the device, e.g. 'Cisco 2911'
        """
        print(f"get_model is implemented on {self.__class__.__name__}")

    @abstractmethod
    def get_interfaces(self) -> List[Interface]:
        """
        Get a list of interfaces on the device, returned as a list of Interface objects
        """
        print(f"get_interfaces is implemented on {self.__class__.__name__}")

    @abstractmethod
    def get_arp_table(self) -> List[ArpEntry]:
        """
        Construct a list of neighbors from the ARP table, returned as a list of Neighbor objects
        """
        print(f"get_arp_table is implemented on {self.__class__.__name__}")

    @abstractmethod
    def get_lldp_neighbors(self) -> List[LldpNeighbor]:
        """
        Construct a list of neighbors from the LLDP table, returned as a list of Neighbor objects
        """
        print(
            f"get_lldp_neighbors is implemented on {self.__class__.__name__}")

    @abstractmethod
    def get_license(self) -> str:
        """
        Get the license information of the device, e.g. 'Cisco IOS Software [Fuji], ISR Software (X86_64_LINUX_IOSD-UNIVERSALK9-M), Version 16.9.4, RELEASE SOFTWARE (fc1)'
        """
        print(f"get_license is implemented on {self.__class__.__name__}")
