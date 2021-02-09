#!/usr/bin/python
__version__ = 0.1
import sys,argparse

parser = argparse.ArgumentParser(description='Transform MAC addresses into common formats')
parser.add_argument('infile', default=sys.stdin, type=argparse.FileType('r'),nargs='?', help="stdin")
parser.add_argument('-i','--input', metavar="00.11:33-ab:cdef", type=str, help="MAC address -:. Characters will be stripped")
parser.add_argument('-f','--format',metavar="[linux,cisco,aruba]", type=str, help="Destination format. Blank generates all")
args = parser.parse_args()


def strip_mac(original_mac):
    result =  original_mac.translate({ord(i): None for i in ':.-\n'})
    if len(result) == 12:
        return result
    else:
        print (original_mac, "is no valid MAC address")
        sys.exit(1)

def plain_to_cisco(mac_plain):
    cisco_mac = mac_plain[:4]+'.'+mac_plain[4:8]+'.'+mac_plain[8:]
    return (cisco_mac)

def plain_to_linux(mac_plain):
    linux_mac = mac_plain[:2]+':'+mac_plain[2:4]+':'+mac_plain[4:6]+':'+mac_plain[6:8]+':'+mac_plain[8:10]+':'+mac_plain[10:]
    return (linux_mac)

def plain_to_aruba(mac_plain):
    aruba_mac = mac_plain[:6]+'-'+mac_plain[6:]
    return (aruba_mac)

def main():
    mac_plain = strip_mac(args.infile.read())
    print (mac_plain)
    #mac_plain = strip_mac(args.input)
    if args.format == "cisco":
        print (plain_to_cisco(mac_plain))
    elif args.format == "linux":
        print (plain_to_linux(mac_plain))
    elif args.format == "aruba":
        print (plain_to_aruba(mac_plain))
    else:
        print ("No known destination format specified. Generating all...")
        print (plain_to_cisco(mac_plain))
        print (plain_to_linux(mac_plain))
        print (plain_to_aruba(mac_plain))

if __name__ == "__main__":
    main()