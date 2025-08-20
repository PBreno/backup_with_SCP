import os
import shutil
import datetime

from paramiko.ecdsakey import ECDSAKey
from scp import SCPClient, SCPException
from paramiko import AuthenticationException, SSHClient, AutoAddPolicy, RSAKey, SSHException
from tqdm import tqdm

class Server:

    def __init__(self, host:str, username:str, password:str ):
        self.host = host
        self.username = username
        self.password = password
        self.client = None


    def get_connection(self) -> SSHClient | None:


        try:

            client = SSHClient()
            client.load_system_host_keys()
            client.set_missing_host_key_policy(AutoAddPolicy())
            client.connect(
                hostname= self.host,
                username=self.username,
                password=self.password,
                timeout=5000,
            )
            print(f"connected to the host {self.host} successful")
            return client

        except AuthenticationException as e:
            print(e)
            return None


    def create_progress( self, filename:str, size:int, sent):
        # tqdm progress bar instance
        self.progress_bar = tqdm(total=size, unit='B', unit_scale=True, desc=filename)

        self.progress_bar.update(sent - self.progress_bar.n)

        if sent >= size:
            self.progress_bar.close()

    def download_file(self, filepath:str, destinationfolder: str, command:str):

        conn = self.get_connection()

        if conn is None:
            print(conn)
            raise Exception("Client is not connected")

        try:
            print(f"downloading file {filepath} to {destinationfolder}")
            #Starting the process of copy file from server to current directory
            sftp = conn.open_sftp()
            filesize = sftp.stat(filepath).st_size
            progress = tqdm(total=filesize, unit='B', unit_scale=True, desc="Downloading")
            progress.update(filesize - progress.n)

            #with tqdm(total=filesize, unit='B', unit_scale=True, desc="Downloading") as pbar:

            with SCPClient(conn.get_transport(), progress=self.create_progress) as scp:

                #inn,stdout, err =  conn.exec_command(command)
                #stdout.channel.recv_exit_status()
                scp.get(filepath)

            # try:
            #     ...
            #     #conn.exec_command("rm /home/ninjabp/dellstore_backup.sql")
            # except SCPException as e:
            #     print(e)
            # inn, cmd1, err = conn.exec_command("ls -lh")
            # print(cmd1.read().decode())

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


