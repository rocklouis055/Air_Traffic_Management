Hello User :)

Initial step:

	1. Extract the zip file B2_Air_Traffic_Management.zip to some location.
	2. Or copy the B2_Air_Traffic_Management folder to some location.
 	3. Or if downloading from github, no need to extract directly store all files somewhere.

To run Air Traffic Management Application first, follow the installtion steps mentioned in Requirements.md

Now to run the app:
	
	This app can run from any IDE supporting python such as Jupyter Notebook,Jupyter Lab,Visual Studio Code,Pycharm,Anaconda etc or even Command promt,Power Shell or Terminal

	A) Before running the application:
		1. Open Mysql by running:
		 	1.1 In Linux based os use command "sudo /opt/lampp/manager-linux-x64.run"
		 	1.2 In Windows "C:\xampp\xampp-control.exe"
		2. Click Manage Servers
		3. Select MySQL Database
		4. Click Run
		5. Select Apache Web Server
		6. Click Run

	(Follow step either B or c).

	B) Now import the Database 
		1. Open any Web browser and hit the link "http://localhost/phpmyadmin/index.php"
		2. Click "Import" button on top middle.
		3. Click Choose file and select the airtrafficmanagementdb.sql.
		4. Click the Import button at the bottom.
		5. Database Should be imported by now, if not follow step C.

	C) Auto import the database using Python code:
		1. Open Command promt,Power Shell or Terminal in directory "B2_Air_Traffic_Management".
		2. Run command "python3 ./Air_Traffic_Management.AutoDB_Import.py"
		3. Database Should be imported by now.

	D) To run in Notebooks:
		1. Open the notebook in the Folder "B2_Air_Traffic_Management"
		2. Open the "Air_Traffic_Managemengt.ipynb" file.
		3. Run the first cell
		4. Enjoy

	E) To run in Command promt,Power Shell or Terminal:
		1. Open Command promt,Power Shell or Terminal in directory "B2_Air_Traffic_Management".
		2. Run command "python3 ./Air_Traffic_Management.py"
		3. Enjoy

1. Initially we have two user "admin" and "normal", "admin" has all the access to Add, Modify, Delete and Show the tables, "normal" has only access to Add section.
2. Admin Details
	Username : admin
	Password : admin
3. Normal Details
	Username : normal
	Password : normal
4. Login by using either of them and Enjoy :)
