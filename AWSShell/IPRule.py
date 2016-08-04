import ipaddress


class IPRule:
    def __init__(self, cidr, ports, protocol):
        self.cidr = str(ipaddress.ip_network(unicode(cidr)))
        self.protocol = self.lookup_protocol(protocol)
        self.ports = {'FromPort': self.handle_ports(ports)[0], 'ToPort': self.handle_ports(ports)[1]}

    def lookup_protocol(self, protocol):
        plist = {-1: 'all',
                 0: 'hopopt',
                 1: 'icmp',
                 2: 'igmp',
                 3: 'ggp',
                 4: 'ipv4',
                 5: 'st',
                 6: 'tcp',
                 7: 'cbt',
                 8: 'egp',
                 9: 'igp',
                 10: 'bbn-rcc-mon',
                 11: 'nvp-ii',
                 12: 'pup',
                 13: 'argus',
                 14: 'emcon',
                 15: 'xnet',
                 16: 'chaos',
                 17: 'udp',
                 18: 'mux',
                 19: 'dcn-meas',
                 20: 'hmp',
                 21: 'prm',
                 22: 'xns-idp',
                 23: 'trunk-1',
                 24: 'trunk-2',
                 25: 'leaf-1',
                 26: 'leaf-2',
                 27: 'rdp',
                 28: 'irtp',
                 29: 'iso-tp4',
                 30: 'netblt',
                 31: 'mfe-nsp',
                 32: 'merit-inp',
                 33: 'dccp',
                 34: '3pc',
                 35: 'idpr',
                 36: 'xtp',
                 37: 'ddp',
                 38: 'idpr-cmtp',
                 39: 'tp++',
                 40: 'il',
                 41: 'ipv6',
                 42: 'sdrp',
                 43: 'ipv6-route',
                 44: 'ipv6-frag',
                 45: 'idrp',
                 46: 'rsvp',
                 47: 'gre',
                 48: 'dsr',
                 49: 'bna',
                 50: 'esp',
                 51: 'ah',
                 52: 'i-nlsp',
                 53: 'swipe',
                 54: 'narp',
                 55: 'mobile',
                 56: 'tlsp',
                 57: 'skip',
                 58: 'ipv6-icmp',
                 59: 'ipv6-nonxt',
                 60: 'ipv6-opts',
                 62: 'cftp',
                 64: 'sat-expak',
                 65: 'kryptolan',
                 66: 'rvd',
                 67: 'ippc',
                 69: 'sat-mon',
                 70: 'visa',
                 71: 'ipcv',
                 72: 'cpnx',
                 73: 'cphb',
                 74: 'wsn',
                 75: 'pvp',
                 76: 'br-sat-mon',
                 77: 'sun-nd',
                 78: 'wb-mon',
                 79: 'wb-expak',
                 80: 'iso-ip',
                 81: 'vmtp',
                 82: 'secure-vmtp',
                 83: 'vines',
                 84: 'iptm',
                 85: 'nsfnet-igp',
                 86: 'dgp',
                 87: 'tcf',
                 88: 'eigrp',
                 89: 'ospfigp',
                 90: 'sprite-rpc',
                 91: 'larp',
                 92: 'mtp',
                 93: 'ax.25',
                 94: 'ipip',
                 95: 'micp',
                 96: 'scc-sp',
                 97: 'etherip',
                 98: 'encap',
                 100: 'gmtp',
                 101: 'ifmp',
                 102: 'pnni',
                 103: 'pim',
                 104: 'aris',
                 105: 'scps',
                 106: 'qnx',
                 107: 'a/n',
                 108: 'ipcomp',
                 109: 'snp',
                 110: 'compaq-peer',
                 111: 'ipx-in-ip',
                 112: 'vrrp',
                 113: 'pgm',
                 115: 'l2tp',
                 116: 'ddx',
                 117: 'iatp',
                 118: 'stp',
                 119: 'srp',
                 120: 'uti',
                 121: 'smp',
                 122: 'sm',
                 123: 'ptp',
                 124: 'isis',
                 125: 'fire',
                 126: 'crtp',
                 127: 'crudp',
                 128: 'sscopmce',
                 129: 'iplt',
                 130: 'sps',
                 131: 'pipe',
                 132: 'sctp',
                 133: 'fc',
                 134: 'rsvp-e2e-ignore',
                 135: 'mobility header',
                 136: 'udplite',
                 137: 'mpls-in-ip',
                 138: 'manet',
                 139: 'hip',
                 140: 'shim6',
                 141: 'wesp',
                 142: 'rohc'}
        if self.is_positive_int(protocol) and int(protocol) in plist:
            return str(protocol)
        try:
            protocol = (pnum for pnum, pname in plist.items() if pname == protocol).next()
            return str(protocol)
        except StopIteration:
            raise Exception(
                "Invalid protocol {}.\nPlease consult https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml".format(
                    protocol))

    def handle_ports(self, ports):
        if self.protocol == "1":  # ICMP
            return [-1, -1]
        if ports == "all":
            return [0, 65535]
        if ports == "-1":  # For all ICMP types
            return [int(ports), int(ports)]
        parsed_ports = ports.split('-')
        parsed_ports = [int(parsed_ports[0]), int(parsed_ports[1]) if len(parsed_ports) > 1 else int(parsed_ports[0])]
        failure_conditions = [
            (parsed_ports[0] < 0 or parsed_ports[0] > parsed_ports[1] or parsed_ports[0] > 65535),
            (parsed_ports[1] < parsed_ports[0] or parsed_ports[1] > 65535)
        ]
        if True in failure_conditions:
            raise Exception("Malformed ports....")
        return parsed_ports

    def is_positive_int(self, val):
        try:
            int(val)
            return True
        except ValueError:
            return False
