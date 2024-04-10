class RouterSSH():
    ipv4: str

    def __init__(self, ipv4):
        self.ipv4 = ipv4

    def get_hostname(self) -> str:
        print(f"get_hostname is implemented on {self.__class__.__name__}")

    def get_model(self) -> str:
        print(f"get_hostname is implemented on {self.__class__.__name__}")

    def get_interfaces(self):
        print(f"get_interfaces is implemented on {self.__class__.__name__}")

    def get_arp_table(self):
        print(f"get_arp_table is implemented on {self.__class__.__name__}")
