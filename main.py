# This is a sample Python script.
from config import SSH_USERNAME, SSH_PASSWORD, SSH_REMOTE_HOST, SSH_FILEPATH, DESTINATION_FOLDER, SSH_KEY_FILEPATH,  SSH_COMMAND
from server import Server


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    server = Server(SSH_REMOTE_HOST,
                    SSH_USERNAME,
                    SSH_PASSWORD,
                    SSH_KEY_FILEPATH)

    server.download_file(SSH_FILEPATH, DESTINATION_FOLDER,SSH_COMMAND, SSH_PASSWORD)
