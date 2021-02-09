#!/usr/bin/python
__version__ = 0.3
import sys
import argparse
import re
from termcolor import colored

parser = argparse.ArgumentParser(description='Transform MAC addresses into common formats')
parser.add_argument('infile', default=sys.stdin, type=argparse.FileType('r'),nargs='?', help="read MACs from stdin")
parser.add_argument('-i','--input', metavar="00.11:33-ab:cdef", type=str, help="one MAC address")
parser.add_argument('-f','--format',metavar="[linux,cisco,aruba]", type=str, help="Destination format")
args = parser.parse_args()

def strip_mac(original_mac):
    result =  original_mac.translate({ord(i): None for i in ':.-\n\r'}).lower()
    if re.match("[0-9a-f]{12}$", result):
        if len(result) == 12:
            return result

def plain_to_cisco(mac_plain):
    cisco_mac = mac_plain[:4]+'.'+mac_plain[4:8]+'.'+mac_plain[8:]
    return (cisco_mac)

def plain_to_linux(mac_plain):
    linux_mac = mac_plain[:2]+':'+mac_plain[2:4]+':'+mac_plain[4:6]+':'+mac_plain[6:8]+':'+mac_plain[8:10]+':'+mac_plain[10:]
    return (linux_mac)

def plain_to_aruba(mac_plain):
    aruba_mac = mac_plain[:6]+'-'+mac_plain[6:]
    return (aruba_mac)

def convert(mac_plain):
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

def validate_input_and_convert(stdin_mac):
    mac_plain = strip_mac(stdin_mac)
    if mac_plain:
        convert(strip_mac(mac_plain))
    else:
        print(colored((stdin_mac.strip(), "is no valid MAC"), 'red'), file=sys.stderr)

def main():
    got_input = None
    if not sys.stdin.isatty():
        got_input = True
        for stdin_mac in args.infile:
            validate_input_and_convert(stdin_mac)
    if args.input: 
        validate_input_and_convert(args.input)
        got_input = True
    else:
        if not got_input:
            print ("no CLI or STDIN input")

if __name__ == "__main__":
    main()