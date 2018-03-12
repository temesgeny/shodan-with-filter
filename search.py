class Host:
    def __init__(self, ip):
        self.set_ip(ip)
        self.ports = []
        self.port_banners = {}
        self.port_service_type = {}

    def set_ip(self, ip):
        if "%3A" in ip:
            self.ip = ip.replace("%3A", ":")
            self.host_type = "IPV6"
        else:
            self.ip = ip
            self.host_type = "IPV4"

    def add_port(self, port):
        self.ports.append(port)

    def set_port_banner(self, port, banner):
        self.port_banners[port] = banner

    def set_port_service_type(self, port, service_type):
        self.port_service_type[port] = service_type

    def __str__(self):
        return str(self.ip)

    def __repr__(self):
        return str(self.ip)

    def __eq__(self, other):
        if type(other) == Host:
            return self.ip == other.ip
        elif type(other) == str:
            return self.ip == other
        return False