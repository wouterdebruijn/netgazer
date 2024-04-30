from abc import ABC, abstractmethod
from typing import List


class Interface():
    name: str
    ipv4: str | None
    ipv4_mask: int | None
    physical: str
    protocol: str

    def __init__(self, name, ipv4, physical, protocol):
        self.name = name
        self.ipv4 = ipv4
        self.physical = physical
        self.protocol = protocol


class Neighbor():
    name: str
    ipv4: str
    interface_name: str


class RouterSSH(ABC):
    ipv4: str

    def __init__(self, ipv4):
        self.ipv4 = ipv4

    @abstractmethod
    @staticmethod
    def vendor_match(vendor: str) -> bool:
        return vendor.lower() == 'huawei'

    @abstractmethod
    def get_hostname(self) -> str:
        """
        Get the hostname of the device, e.g. 'router1'
        """
        print(f"get_hostname is implemented on {self.__class__.__name__}")

    @abstractmethod
    def get_model(self) -> str:
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
    def get_arp_table(self) -> List[Neighbor]:
        """
        Construct a list of neighbors from the ARP table, returned as a list of Neighbor objects
        """
        print(f"get_arp_table is implemented on {self.__class__.__name__}")

    @abstractmethod
    def get_lldp_neighbors(self) -> List[Neighbor]:
        """
        Construct a list of neighbors from the LLDP table, returned as a list of Neighbor objects
        """
        print(
            f"get_lldp_neighbors is implemented on {self.__class__.__name__}")
