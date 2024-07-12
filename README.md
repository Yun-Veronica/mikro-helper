# mikro-helper docs
This tool automates the process of creating backups on Mikrotik network devices using SSH and Paramiko in Python.

## Requirements
Make sure you have Python 3.x and pip (``sudo apt install python3-pip``) installed 
along with the necessary packages listed in `requirements.txt`(`pip install - r requirements.txt`).

## Files Usage

In searching of arguments for ssh conection it goes in the following priority (except for host ip address, it ca be specified only in host.yml):
1. k
2. k
3. k

## Run on the Ubuntu server
1. Clone code from the repository:</br>
``
git clone https://github.com/Yun-Veronica/mikro-helper.git
``
2. Create .venv </br>
``
cd mikro-helper
sudo apt install python3-pip
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
``

3. Make mikro-helper.py executable </br>
``
chmod +x path/to/file/mikro-helper.py
``
</br> For example: I am currently in home/ folder. Then, for my situation, the command will be like this: </br>
``
chmod +x mikro-helper/mikro-helper.py
``
4. Run </br>
``
python3 path/to/file/mikro-helper.py
``
</br >If I am currently in home/ folder. Then, for my situation, the command will be like this: </br>
``
python3  mikro-helper/mikro-helper.py
``