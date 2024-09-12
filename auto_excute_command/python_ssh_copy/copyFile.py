import paramiko, os

ip = "10.239.12.235"
user = "general"
password = "Passw0rd"
local_filepath = r"C:\PY\IPU\CXSH\null"
remote_filepath = r"C:\Users\General\Desktop\IPU\autoCMD\2024-08-28\logfile_descriptions_p_2024-08-28-17-47-30.log"

transport = paramiko.Transport((f"{ip}", 22))
transport.connect(username=user, password=password)

sftp = paramiko.SFTPClient.from_transport(transport)

# sftp.put(f'{local_filepath}', f'{remote_filepath}')
sftp.get(remote_filepath, os.path.join(local_filepath, 'logfile_descriptions_p_2024-08-28-17-47-30.log'))
transport.close()
