import winutils
import os
import datetime

# Packages for Backup file generation
import subprocess
import logging

# Leaf directory
now = datetime.datetime.today()
timestamp = now.strftime('%d-%m-%Y_%H-%M-%S')
directory = timestamp

# Source path
fromDirectory = [r"replace with your Source path"]

# Parent Directories
parent_dir = r"replace with your destination path"

# Path
path = os.path.join(parent_dir, directory)

# Create the directory
os.makedirs(path)

# Destination path
toDirectory = [path]

# define postgres sql detail here
postgres_host = "replace with your hostname"
postgres_port = "replace with your portnumber"
postgres_db = "replace with your batabase name"
postgres_user = "replace with your username"
postgres_password = "replace with your password"


# where to store
manager_config = {
    'BACKUP_PATH': toDirectory[0],
}

# Copy paste function
def copy_paste():
    try:
        for i in range(len(fromDirectory)):
            winutils.copy(src=os.path.abspath(fromDirectory[i]), dst=os.path.abspath(toDirectory[i]))

    except Exception as e:
        print(e)


# Postgres Backup Function
def backup_postgres_db(host, database_name, port, user, password, dest_file):
    """
    Backup postgres db to a file.
    """

    try:
        process = subprocess.Popen(
            ['pg_dump',
             '--dbname=postgresql://{}:{}@{}:{}/{}'.format(user, password, host, port, database_name),
             '-Fc',
             '-f', dest_file,
             '-v'],
            stdout=subprocess.PIPE,
            # Uncomment following line if gives "file not found" error
            # shell=True,
        )
        output = process.communicate()[0]
        if int(process.returncode) != 0:
            print('Command failed. Return code : {}'.format(process.returncode))
            exit(1)
        return output
    except Exception as e:
        print(e)
        exit(1)

def main():

    # Call copy paste function
    copy_paste()

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    try:
        timestr = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
        filename = 'backup-{}-{}.sql'.format(timestr, postgres_db)
        local_file_path = '{}/{}'.format(manager_config.get('BACKUP_PATH'), filename)
        logger.info('Backing up {} database to {}'.format(postgres_db, local_file_path))

    except Exception as e:
        print(e)

    # Call postgres backup function
    try:
        result = backup_postgres_db(postgres_host,
                                    postgres_db,
                                    postgres_port,
                                    postgres_user,
                                    postgres_password,
                                    local_file_path)
        for line in result.splitlines():
            logger.info(line)

    except Exception as e:
        print(e)

    logger.info("Backup complete")
    logger.info("Compressing {}".format(local_file_path))


if __name__ == '__main__':
    main()

