"""Module to save the IPs list to specific file."""

import os


FILES_DIR = 'files/'
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
PARENT_DIR = os.path.abspath(os.path.join(BASE_DIR, os.pardir))
DEST_DIR = os.path.join(PARENT_DIR, FILES_DIR)


def save_addresses_file(file_name: str, addresses: list, port: int):
    """
    Function that saves IP list to the appropriate file
    in the files directory.
    :param file_name: name of the file for saving.
    :param addresses: list of IP addresses.
    :param port: port to connect to the certain IP.
    :return: None
    """
    with open(f'{DEST_DIR}{file_name}', 'w') as file:
        for address in addresses:
            file.write(f'{address}:{port} \n')
