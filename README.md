# mikro-helper docs

This tool automates the process of creating backups on Mikrotik network devices using SSH and Paramiko in Python.

## Files Usage

In searching of arguments for ssh connection it goes in the following priority (except for host ip address, it ca be
specified only in host.yml):

1. hosts/{group_name}.yaml
2. vars/{group_name}.ini

Replace file content as in examples but with your data.
In vars/ and hosts/ files should be named after groups that are
saved in them. 

## Run on the Ubuntu server

1. Clone code from the repository:</br>
   ``
   git clone https://github.com/Yun-Veronica/mikro-helper.git 
   ``
2. Change directory to mikro-helper and install .deb package with dpkg: </br>
```
cd mikro-helper
sudo dpkg -i mikro-helper.deb
```
3. Change files in hosts/ and vars/ according to your needs </br>
4. Run program using mikro-helper command: </br>
```mikro-helper```

Also you can run program with optional params and specify there names of groups that you want to run. For example : </br>
```mikro-helper -o group_name ```
