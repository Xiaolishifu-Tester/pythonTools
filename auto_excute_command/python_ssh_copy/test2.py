import os, stat
import paramiko

ip = "10.239.12.235"
ssh_port = 22
user = "general"
password = "Passw0rd"
local_filepath = r"C:\PY\IPU\CXSH\null"
remote_filepath = r"C:\Users\General\Desktop\IPU\autoCMD\2024-08-28"


# ??SSH???
ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(ip, ssh_port, user, password)

# ??SFTP???
sftp_client = ssh_client.open_sftp()

# ??????????
def copy_remote_folder_to_local(remote_path, local_path, sftp_client):
    files_and_folders = sftp_client.listdir_attr(remote_path)
    for item in files_and_folders:
        remote_item_path = os.path.join(remote_path, item.filename)
        local_item_path = os.path.join(local_path, item.filename)
        print(item.st_mode)
        if stat.S_ISDIR(item.st_mode):  # ???????????
        # if os.stat(item.st_mode):  # ???????????
            os.mkdir(local_item_path)
            copy_remote_folder_to_local(remote_item_path, local_item_path, sftp_client)
        else:  # ???????????
            sftp_client.get(remote_item_path, local_item_path)

copy_remote_folder_to_local(remote_filepath, local_filepath, sftp_client)

# ??SFTP?SSH???
sftp_client.close()
ssh_client.close()