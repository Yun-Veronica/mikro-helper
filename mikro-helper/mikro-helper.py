#!/usr/bin/env python3

import datetime
import paramiko
import yaml
import argparse
import os
from configparser import ConfigParser

def ini_read(filename):
    '''
    Reads configurations from an INI file and returns them as a dictionary.

    :param filename: str, Name of the INI file.
    :return: dict, A dictionary containing sections and their configurations from the INI file.
    '''

    data_from_ini = {}
    config = ConfigParser(allow_no_value=True)

    config.read(filename)

    sections = config.sections()

    for section in sections:
        data_from_ini[section] = dict(config[section])

    return data_from_ini


def yaml_read(filename):
    '''
     Reads configurations from a YAML file and returns them as a dictionary.

    :param filename:  str, Name of the YAML file.
    :return: dict, A dictionary containing parsed YAML data.
    '''

    with open(filename, 'r') as file:
        return yaml.safe_load(file)


def get_filenames(dir_path):
    '''
    Getting filenames from directory
    :param dir_path: path to the directory
    :return: filenames
    '''
    filenames = os.listdir(dir_path)
    return filenames


CONFIG_DATA = ini_read("conf.ini")
FILES_PATHS = CONFIG_DATA.get('folder_paths', None)


def get_hosts_groups(host_filename=""):
    """
    Reads host groups from YAML files in the specified directory or a specific YAML file.

    If a specific host filename is provided, it reads and returns the data from that file.
    Otherwise, it reads all YAML files in the specified directory and organizes the host data into groups.

    :param host_filename: host_filename (str): Optional. The name of a specific host file to read. Default is an empty string.

    :return:
    dict: A dictionary where keys are group names (derived from filenames without extensions) and values are dictionaries of host parameters.
    """
    hosts_dir_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'hosts')

    if FILES_PATHS:
        hosts_dir_path = FILES_PATHS.get('hosts_folder_path', os.path.join(os.path.dirname(os.path.realpath(__file__)), 'hosts'))

    return process_host_file(hosts_dir_path, host_filename)


def process_host_file(hosts_dir_path, filename):
    """
    Processes a single .ini file and returns the host data.

    :param hosts_dir_path (str): Path to the directory containing the host files.
    :param filename (str): Name of the .ini file to process.

    :returns
    dict: A dictionary of host parameters.
    """
    hosts_data = ini_read(os.path.join(hosts_dir_path, filename))
    host_data = {}

    for hosts in hosts_data:
        for host in hosts_data[hosts]:
            if len(host.split()) > 1:
                data = f"{host}={hosts_data[hosts][host]}".split(' ')
                params_dict = {}
                for i in data:
                    if '=' in i:
                        key, val = i.strip().split("=")
                        params_dict[key] = val.strip("'").strip('"')
                host_data[data[0]] = params_dict
            else:
                host_data[host] = {'port': "", "username": "", "password": ""}

    return host_data


# print(process_host_file('./hosts', 'group1.ini'))
# breakpoint()
#

def get_vars_groups(vars_filename=""):
    '''
    getting dict with
    :param vars_filename:
    :return:
    '''
    vars_dir_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'vars')
    if FILES_PATHS:
        vars_dir_path = FILES_PATHS.get('vars_folder_path', os.path.join(os.path.dirname(os.path.realpath(__file__)), 'vars'))

    return process_vars_file(vars_dir_path, vars_filename)


def process_vars_file(vars_dir_path, filename):
    vars_data = ini_read(os.path.join(vars_dir_path, filename))
    host_vars_data = {}

    for host in vars_data:
        params = vars_data[host]
        port = params.get('port', '22').strip().strip('"').strip("'")
        username = params.get('user', 'admin').strip().strip('"').strip("'")
        password = params.get('password', '12356').strip().strip('"').strip("'")

        host_vars_data[host] = {"port": port, 'username': username, 'password': password}

    return {filename.strip('.ini'): host_vars_data}


def build_command_params_dict(group_name=''):
    '''
     Constructs command parameters for each host based on configurations from YAML and INI files.

    :param group_name:  Optional
        If empty = all groups are called
        If not empty = only mentioned group`s  devices are called

    :return: dict
         A dictionary mapping group names to dictionaries of command parameters for each host.
    '''
    # Global timestamp for backup filenames
    time_stamp = str(datetime.datetime.now().date()) + " " + str(datetime.datetime.now().time())

    parsed_config = ini_read("conf.ini")
    if parsed_config:
        backup_filename = parsed_config['default_params'].get('backup_filename', 'backup' + time_stamp)
        backup_password = parsed_config['default_params'].get('backup_password', '123456')
    else:
        backup_filename = 'backup ' + time_stamp
        backup_password = '123456'

    if group_name:
        groups_dict = [group_name]
    else:
        hosts_dir_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'hosts')
        if FILES_PATHS:
            hosts_dir_path = FILES_PATHS.get('hosts_folder_path', os.path.join(os.path.dirname(os.path.realpath(__file__)), 'hosts'))

        groups_dict = [i.strip(".ini") for i in get_filenames(hosts_dir_path)]

    command_params_dict = {i: {} for i in groups_dict}
    for group in groups_dict:

        group_hosts = get_hosts_groups(f'{group}.ini')
        group_vars = get_vars_groups(f'{group}.ini')

        for host in group_hosts:
            # Priority level: params in host/,host params in vars/, group params in vars/

            # check if we had specified this host in vars directly
            if group_vars[group].get(host):
                host_vars = group_vars[group]

                if not group_hosts[host].get('port'):
                    port = host_vars.get('port')
                else:
                    port = group_hosts[host]['port']

                if not group_hosts[host].get('user'):
                    username = host_vars.get('user')
                else:
                    username = group_hosts[host]['user']

                if not group_hosts[host].get('password'):
                    password = host_vars.get('password')
                else:
                    password = group_hosts[host]['password']

            else:
                if not group_hosts[host].get('port'):
                    port = group_vars[group][group].get('port')
                else:
                    port = group_hosts[host]['port']

                if not group_hosts[host].get('user'):
                    username = group_vars[group][group].get('user')
                else:
                    username = group_hosts[host]['user']

                if not group_hosts[host].get('password'):
                    password = group_vars[group][group].get('password')
                else:
                    password = group_hosts[host]['password']

            command_params_dict[group].setdefault(host, {'hostname': host, 'port': port, 'username': username,
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

    command = f'system backup save name="{backup_filename}" password="{backup_password}" encryption=aes-sha256'
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
    hosts_dir_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'hosts')
    if FILES_PATHS:
        hosts_dir_path = FILES_PATHS.get('hosts_folder_path', os.path.join(os.path.dirname(os.path.realpath(__file__)), 'hosts'))

    hosts_groups = get_filenames(hosts_dir_path)

    # breaking into hosts_groups
    if group_name.lower() == "all" or group_name == '':
        devices_dict = build_command_params_dict()
    elif group_name in hosts_groups.keys():
        devices_in_group = hosts_groups.get(group_name, "Error")

        devices_dict = {device_conf: build_command_params_dict(device_conf)[device_conf] for device_conf in
                        devices_in_group.keys()}

    else:
        print("Error: unknown group name")
        return

    for device_group in devices_dict:
        for device_ip in devices_dict[device_group]:
            # print(device_ip, devices_dict[device_group][device_ip])
            print(device_ip, execute_backup_command_on_device(**devices_dict[device_group][device_ip]))
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

