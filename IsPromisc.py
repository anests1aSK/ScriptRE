import os

NET_DEVICE_PATH = '/sys/devices/virtual/net/'
IFF_PROMISC = 0x100

def print_results(table):
    header = [('Device', 'Promisc Mode'), ('------', '---------------')]
    table = header + table
    col_width = [max(len(x) for x in col) for col in zip(*table)]
    for line in table:
        print "| " + " | ".join("{0:{1}}".format(x, col_width[i])
                                for i, x in enumerate(line)) + " |"

def iterate_and_determine_promisc():
    device_promisc = []
    for device in os.listdir(NET_DEVICE_PATH):
        with open(os.path.join(NET_DEVICE_PATH, device, 'flags')) as f:
            device_flags = f.read()
            if device_flags:
                if int(hex(int(device_flags, 16) & IFF_PROMISC), 16):
                    device_promisc.append((device, 'ON'))
                else:
                    device_promisc.append((device, 'OFF'))
            else:
                device_promisc.append((device, 'UNKNOWN'))

    print_results(device_promisc)

iterate_and_determine_promisc()