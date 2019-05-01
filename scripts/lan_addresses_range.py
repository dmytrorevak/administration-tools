"""Module to get all possible LAN IP addresses."""

import re
import subprocess
from subprocess import CompletedProcess
from typing import Iterator, List

import netifaces

from files_helper import save_addresses_file


ARP_SCAN_COMMAND = "sudo arp-scan --localnet"
IP_PATTERN = re.compile(r"(?:\d{0,3}\.){3}\d{0,3}")
LAN_ADDRESSES_FILE_NAME = 'hosts'
SSH_PORT = 22


def parse_bash_command(command, *args):
    """
    Function that decomposes the bash string command to the list for
    calling it by subprocess module.

    :param command: the string of bash command.
    :param args: the all possible arguments fo the accepted command.
    :return: list with the bash command building blocks.
    """
    command_arguments = command.split(" ")
    command_arguments.extend(args)
    return command_arguments


def get_host_interfaces() -> List[str]:
    """
    Function which provides the all current host interfaces.
    :return: list with host interfaces.
    """
    return netifaces.interfaces()


def get_arp_scan_interface_keys(interfaces: List[str]) -> Iterator[str]:
    """
    Function that creates the correct string key with each
    interface for the arp-scan command.
    :return: generator with created keys.
    """
    return (f"--interface={iface}" for iface in interfaces)


def parse_arp_scan_output(completed_process: CompletedProcess) -> List[str]:
    """
    Function that parses the completed process of the subprocess module.
    Parsing provided by using the re module.
    :param completed_process: finished subprocess instance.
    :return: the list with parsed IPs or the empty list.
    """
    result = []
    if not completed_process.returncode:
        output = str(completed_process.stdout)
        ip_matches = IP_PATTERN.finditer(output)
        result.extend([match.group() for match in ip_matches])
    return result


def get_lan_ips() -> list:
    """
    Function that returns the complete list of IP addresses
    of all host interfaces.
    :return: list with all possible IP addresses.
    """
    lan_ips = []
    interfaces = get_host_interfaces()
    for iface_key in get_arp_scan_interface_keys(interfaces):
        command = parse_bash_command(ARP_SCAN_COMMAND, iface_key)
        completed_process = subprocess.run(command, capture_output=True)
        lan_ips.extend(parse_arp_scan_output(completed_process))
    return lan_ips


def main():
    """
    Main script function.
    :return: None
    """
    try:
        ips = get_lan_ips()
        print("Found the following IPs: ", ips)
        save_addresses_file(LAN_ADDRESSES_FILE_NAME, ips, SSH_PORT)
        print(f"Saved IPs to {LAN_ADDRESSES_FILE_NAME} "
              f"file in files/ directory")
    except (FileNotFoundError, RuntimeError) as error:
        print(f"The script failed with following exception: {error}")


if __name__ == "__main__":
    main()
