import os
import shutil
import datetime

from paramiko.ecdsakey import ECDSAKey
from scp import SCPClient, SCPException
from paramiko import AuthenticationException, SSHClient, AutoAddPolicy, RSAKey, SSHException


class Server:

    def __init__(self, host, username, password, ssh_key_filepath: str):
        self.host = host
        self.username = username
        self.password = password
        self.ssh_key_filepath = ssh_key_filepath
        self.client = None


    def get_connection(self) -> SSHClient | None:

        print("Starting SSH connection")

        try:

            client = SSHClient()
            client.load_system_host_keys()
            client.set_missing_host_key_policy(AutoAddPolicy())
            client.connect(
                hostname= self.host,
                username=self.username,
                password=self.password,
                key_filename=self.ssh_key_filepath,
                timeout=5000,
            )

            return client

        except AuthenticationException as e:
            print(e)
            return None


    def download_file(self, filepath:str, destinationfolder: str, command:str, password:str):

        conn = self.get_connection()

        if conn is None:
            print(conn)
            raise Exception("Client is not connected")

        try:

            #Starting the process of copy file from server to current directory
            scp = SCPClient(conn.get_transport())

            inn,stdout, err =  conn.exec_command(command)
            stdout.channel.recv_exit_status()
            scp.get(filepath)

            # If there is more than 3 backup, remove all of them to startup a new cycle of storage
            if len(os.listdir(destinationfolder)) > 2:
                 for file in os.listdir(destinationfolder):
                     print('Removing : ', file)
                     os.remove(f"{destinationfolder}\\{file}")

            #Move the backup to another folder
            db_backup= [ file for file in os.listdir() if file.endswith(".sql") ]
            renamed_db = db_backup[0].replace(".sql","")
            renamed_db = renamed_db + "-" + datetime.datetime.now().strftime("%Y%m%d-%H%M") +".sql"
            os.renames(db_backup[0], renamed_db)
            currentdirectory = os.path.join(os.getcwd(), renamed_db)
            move = shutil.move(currentdirectory, destinationfolder)

            print(f"Moving file to destination folder {move}")

            #Close the connection
            conn.close()
        except SCPException as e:
            raise e


