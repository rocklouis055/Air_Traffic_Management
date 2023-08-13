To run this application, you should have Python and MqSQL installed on the system

A) To install Python (version >=3), follow the link :
	https://www.python.org/downloads/

B) To install MySQL, follow the link :
	https://dev.mysql.com/downloads/installer/

Now you should have pip or pip3 installed to install the Python dependencies, Mostly it will be auto installed with Python , if not, it can be installed as

	For Linux/Ubuntu based OS :
		sudo apt-get -y install python3-pip

	For Windows OS :
		curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
		python3 get-pip.py

(Run either C,D or E)

C) Requiremnts on a Linux/Ubuntu Desktop

	1. Firstly install Python Pillow Library using 
		pip3 install Pillow
	2. Now install MySQL Linux/Client using
		sudo apt-get install libmysqlclient-dev
	3. Now install Python MySQL Connector/Driver
		pip3 install mysql-connector
	4. Now install Python Tkinter using
		pip3 install tk
	5. Now install Python Tkinter Calender widget using
		pip3 install tkcalendar

D) Requiremnts on a Windows Desktop

	1. Firstly install Python Pillow Library using 
		python3 -m pip install Pillow
	2. Now install Python MySQL Connector/Driver
		python3 -m pip install mysql-connector-python
	3. Now install Python Tkinter using
		python3 -m pip install tk
	4. Now install Python Tkinter Calender widget using
		python3 -m pip install tkcalendar

E) To auto install Python dependencies
	1. Open Command promt,Power Shell or Terminal in directory "B2_Air_Traffic_Management".
	2. Run command "python3 ./Requirements.py"
	3. Enjoy
	
Note : pip3 is for python3 and for lower version , pip can be used

E) MySQL Database that we use can be installed by importing airtrafficmanagementdb.sql in MySQL or by running python3 airtraffic.py (See step (A))

F) Enjoy the app :)
