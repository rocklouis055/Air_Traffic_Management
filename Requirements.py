from sys import platform
import os
if platform == "linux" or platform == "linux2":
    print("Linux or Linux based OS Detected.\nInstalling as by the OS")
    cmd=["pip3 install Pillow",
     "sudo apt-get install libmysqlclient-dev",
     "pip3 install mysql-connector",
     "pip3 install tk",
     "pip3 install tkcalendar"]
    for i in cmd:
        os.system(i)
elif platform == "win32":
    print("Windows OS Detected.\nInstalling as by the OS")
    cmd=["python3 -m pip install Pillow",
         "python3 -m pip install mysql-connector-python",
         "python3 -m pip install tk",
         "python3 -m pip install tkcalendar"]
    for i in cmd:
        os.system(i)
else:
    print("Other OS detected,Please install manually the required files.")