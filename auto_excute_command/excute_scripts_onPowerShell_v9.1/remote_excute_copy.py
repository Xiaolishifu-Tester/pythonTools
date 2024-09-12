import paramiko, stat, os, time
from datetime import datetime

# ????????IP?????????
remote_host = "10.239.12.235"
username = "general"
password = "Passw0rd"
local_filepath = os.getcwd()
remote_filepath = r"C:\Users\General\Desktop\IPU\autoCMD"
remote_folder = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d-%H-%M-%S')[:10]

ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# ????????
ssh_client.connect(remote_host, username=username, password=password)
sftp_client = ssh_client.open_sftp()
def auto_excute(py, args):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # ????????
    ssh_client.connect(remote_host, username=username, password=password)
    # ??SSH???
    # ??SCPClient??????
    stdin, stdout, stderr = ssh_client.exec_command( fr"C: &cd {remote_filepath} &python {py} {args}")
    # stdin, stdout, stderr = ssh_client.exec_command( fr"C: &cd {remote_filepath} &python auto_run_cxsh_latest_gnripu_0302.py --p --H0302 --CR-mt")
    # scp_client = paramiko.SFTPClient(client.get_transport())
    # result = stdout.read()
    # print(result.decode())
    exit_status = stdout.channel.recv_exit_status()
    # if exit_status == 0:
    #     print("脚本运行完毕")
    # else:
    #     print("远程脚本执行失败")
    ssh_client.close()
    return  exit_status


def copy_remote_folder_to_local(remote_path, local_path, sftp_client):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # ????????
    ssh_client.connect(remote_host, username=username, password=password)
    sftp_client = ssh_client.open_sftp()
    # ??SFTP???
    files_and_folders = sftp_client.listdir_attr(remote_path)
    for item in files_and_folders:
        remote_item_path = os.path.join(remote_path, item.filename)
        local_item_path = os.path.join(local_path, item.filename)
        if stat.S_ISDIR(item.st_mode):  # ???????????
            # if os.stat(item.st_mode):  # ???????????
            os.mkdir(local_item_path)
            copy_remote_folder_to_local(remote_item_path, local_item_path, sftp_client)
        else:  # ???????????
            sftp_client.get(remote_item_path, local_item_path)


result_code = auto_excute("auto_run_cxsh_latest_gnripu_0302.py", "--p --H0302 --CR-mt")
if result_code ==0:
    copy_remote_folder_to_local(rf"{remote_filepath}\{remote_folder}", local_filepath, sftp_client)
    # closed sftp connnect
    sftp_client.close()
    ssh_client.close()