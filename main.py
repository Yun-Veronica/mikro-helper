#!/usr/bin/env python3

import datetime
import paramiko
import yaml
import argparse
from configparser import ConfigParser


def ini_read(filename='groups.ini'):
    '''
    Reads configurations from an INI file and returns them as a dictionary.

    :param filename: str, optional. Name of the INI file (default is 'groups.ini').
    :return: dict, A dictionary containing sections and their configurations from the INI file.
    '''

    data_from_ini = {}
    config = ConfigParser(allow_no_value=True)

    config.read(filename)

    sections = config.sections()

    for section in sections:
        data_from_ini[section] = dict(config[section])

    return data_from_ini


def yaml_read(filename='hosts.yml'):
    '''
     Reads configurations from a YAML file and returns them as a dictionary.

    :param filename:  str, optional
        Name of the YAML file (default is 'hosts.yml').
    :return: dict, A dictionary containing parsed YAML data.
    '''

    with open(filename, 'r') as file:
        prime_service = yaml.load(file, Loader=yaml.Loader)
    return prime_service


def build_command_params_dict():
    '''
     Constructs command parameters for each host based on configurations from YAML and INI files.

    :return: dict
         A dictionary mapping group names to dictionaries of command parameters for each host.
    '''
    # Global timestamp for backup filenames
    time_stamp = str(datetime.datetime.now().date()) + " " + str(datetime.datetime.now().time())

    parsed_hosts = yaml_read('hosts.yml')
    parsed_ini = ini_read()
    parsed_config = yaml_read("conf.yaml")
    if parsed_config:
        backup_filename = parsed_config.get('backup_filename', 'backup' + time_stamp)
        backup_password = parsed_config.get('backup_password', '12345678')
        username = parsed_config.get('username', 'admin')
        password = parsed_config.get('password', '123456')
        port = parsed_config.get('port', '22')
    else:
        backup_filename = 'backup ' + time_stamp
        backup_password = '12345678'
        username = 'admin'
        password = '123456'
        port = 22

    command_params_dict = {i: {} for i in parsed_hosts}

    for hosts in parsed_hosts:
        # priority level:  host, ini, conf
        for host in parsed_hosts[hosts]:
            host_with_param = host.split()
            hostname = host_with_param[0]
            if 'port' in parsed_ini.get(hosts + ":vars"):
                port = parsed_ini.get(hosts + ":vars").get('port')
            if 'port' in host_with_param:
                if host_with_param.index('port') != (len(host_with_param) - 1):
                    port = host_with_param[host_with_param.index('port') + 1]

            if 'username' in parsed_ini.get(hosts + ":vars"):
                username = parsed_ini.get(hosts + ":vars").get('username')
            if 'username' in host_with_param:
                if host_with_param.index('username') != (len(host_with_param) - 1):
                    username = host_with_param[host_with_param.index('username') + 1]

            if 'password' in parsed_ini.get(hosts + ":vars"):
                password = parsed_ini.get(hosts + ":vars").get('password')
            if 'password' in host_with_param:
                if host_with_param.index('password') != (len(host_with_param) - 1):
                    password = host_with_param[host_with_param.index('password') + 1]

            command_params_dict[hosts].update({'hostname': hostname, 'port': port, 'username': username,
                                               'password': password, 'backup_filename': backup_filename,
                                               'backup_password': backup_password})

    return command_params_dict


def execute_backup_command_on_device(hostname, port, username, password, backup_filename, backup_password):
    '''
    Executes backup command on a Mikrotik device via SSH using Paramiko.

    :param hostname: str, IP address of the device.
    :param port: int, port number
    :param username: str, username on the device for ssh connection
    :param password: str, password for ssh connection
    :param backup_filename: str, Filename for the backup.
    :param backup_password: str, Password for encrypting the backup.
    :return:  Status message indicating success or error.

    '''

    command = f'system backup save name={backup_filename} password={backup_password} encryption=aes-sha256'
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:

        ssh_client.connect(hostname=hostname, port=port, username=username, password=password, look_for_keys=False,
                           allow_agent=False)
        session = ssh_client.get_transport().open_session()

        session.exec_command(command)
    except Exception as e:
        return f"Error: {e}"
    return "Backup created"


def create_backups_for_devices(group_name="all"):
    '''
    Creates backups for devices based on the specified group name.

    :param group_name: name of devices group to be executed
    :return: None
    '''

    parsed_ini = ini_read()

    # breaking into groups
    if group_name.lower() == "all":
        devices_dict = build_command_params_dict()
    elif group_name in parsed_ini:
        devices_in_group = parsed_ini.get(group_name, "Error")
        all_device_dict = build_command_params_dict()
        if devices_in_group != "Error":
            devices_dict = {device_conf: all_device_dict.get(device_conf) for device_conf in devices_in_group.keys()}
        else:
            print("Error: unknown group name")
            return
    else:
        print("Error: unknown group name")
        return

    for device_ip in devices_dict:
        print(device_ip, execute_backup_command_on_device(hostname=device_ip, **devices_dict[device_ip]))
        return


def main():
    """
    Main function to parse command-line arguments and initiate backup process.
    """

    parser = argparse.ArgumentParser(description='Description of your program')
    parser.add_argument('-o', '--optional_param', type=str, help='Optional parameter')

    args = parser.parse_args()

    # Access optional parameter if provided
    if args.optional_param:
        create_backups_for_devices(args.optional_param)
    else:
        create_backups_for_devices()


if __name__ == '__main__':
    main()
