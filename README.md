# Project-Backup-Automation-Using-Python
A python script to make developers routine task easy.

Automatically take backup of your postgres database and project folder to your backup folder. 

# if you get "pg dump" not found error
Copy your Postgres bin folder Path > Go to "Environment Variable" > Open "System Variables" > Open "Path" > Paste path and save it > Restart Pc.

# requirements
pip install pywinutils

# Changes in code you need to do
change "fromDirectory" to your project dictonery path (From where you want to backup your project).

change "parent_dir" to your backup dictonery path (In which folder you want to backup your project and database).

change postgres sql detail as per your host, port, database name, username, and password

That's all. You are ready to go.

# Run code
  python backup_project.py
