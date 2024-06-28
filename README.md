# PyBackupTool docs
This tool automates the process of creating backups on Mikrotik network devices using SSH and Paramiko in Python.

## Requirements

Make sure you have Python 3.x installed along with the necessary packages listed in `requirements.txt`.

## Files Usage
hosts.yaml - there all of your ip devices groups are written. Also you can specify some variables for ssh conection, such as port, password, or username. <br>
Example: <br>
```
group1:
  - 192.168.2.3 password password

group2:
  - 192.168.2.2 port 22
  - 192.168.2.1
  - 192.168.2.3 username admin

```

groups.ini - INI file, where you can group your groups of devices and specify ssh connection variables such username, password, port for group of devices using [groupname:vars] syntax. <br>
Example: <br>
```
[full_group] #group of devices group
group1
group2
  
[secondary]
group1
  
[group1:vars] #specified variables for group1
username = admin
password = admin
  
[group2:vars]
username = super_admin
password = passsword
 ```
conf.yaml -  in this file you may specify some of the commented parameters and after that uncomment them for usage.Do not rename them<br>


In searching of arguments for ssh conection it goes in the following priority (except for host ip address, it ca be specified only in host.yml):
1. hosts.yml
2. groups.ini
3. conf.yaml
4. default parameters

## Run

