import copy
import os, socket, re, shutil, time


# hostname = socket.gethostname()[:15].upper()
# if not os.path.isdir(r"C:\temp\test_logs"):
hostnames = ["SH23L11001N0202", "SH23L11001N0203","SH23L11001N0204"]  # must be 3
excute_date = input("Please input need to operation date folder: ").upper()
excute_type = input("Please input you excute type: eg: d/delete means delete or r/rename means rename: ").upper()
folder_path = rf"{os.getcwd()}\{excute_date}"
folder_files = os.listdir(folder_path)


def rename():
    print("Your means is rename logs folder, please wait........")
    print("Start rename log folder ......")
    pattern = re.compile(r'^\d')
    os.chdir(folder_path)
    for file in folder_files:
        if os.path.isdir(rf"{folder_path}\{file}"):
            id = file[:11]
            title = file[12:]
            os.chdir(folder_path)
            if bool(pattern.match(file)):
                print(f"rename <<{file}>> to <<{title}>> .......")
                try:
                    os.rename(file, title)
                    print(f"End, rename successfully.......")
                except FileExistsError as r:
                    os.rename(file, f"{title}_2")
                    print(f"End, rename successfully.......")
                except Exception as fail:
                    print(fail)
            else:
                print(fr"Don't need to rename it. ======= file is <<{file}>>")


def delete():
    os.chdir(folder_path)
    number = 0
    print("Upload log to server, need delete other file , save bios log")
    for file in folder_files:
        logs_path = os.path.join(folder_path, file)
        if os.path.isdir(rf"{folder_path}\{file}"):
            print(f"In <<{file}>> folder")
            os.chdir(logs_path)
            for item in os.listdir():
                if os.path.isdir(item):
                    if item != "serial_logs":
                        print(f"=== Delete folder <<{item}>>.......")
                        shutil.rmtree(item)
                        number +=1
                        # print(f"====== Delete folder <<{item}>> successfully...")
                        print(f"========= successfully....")
                    else:
                        os.chdir(rf"{os.getcwd()}\serial_logs")
                        for serial in os.listdir():
                            serial_path = os.path.join(os.getcwd(), serial)
                            # if re.match(parrents2, serial) or serial.startswith("bmc"):
                            # if serial.startswith("bios_serial_reader_raw") or serial.startswith("bmc") :
                            if serial.startswith("bios_serial_reader_raw") or serial.startswith("bmc") or serial.startswith("Process"):
                                print(f"=== Delete file {serial_path} ......")
                                os.remove(serial_path)

                                number +=1
                                print(f"========= successfully....")
                                # print(f"====== Delete file {serial_path} successfully......")
                            else:

                                shutil.copy2(serial_path, logs_path)
                                print(f"=========== Copy {serial_path} to {logs_path} successfully.....")
                else:
                    os.chdir(logs_path)
                    if item.startswith("bios_serial_reader") or item.startswith(f"{hostnames[0]}_20") or item.startswith(f"{hostnames[1]}_20") or item.startswith(f"{hostnames[2]}_20"):
                        pass
                    else:
                        paths = os.path.join(os.getcwd(), item)
                        print(f"=== Delete file {paths} ........")
                        os.remove(paths)
                        number +=1
                        # print(f"====== Delete file {paths} successfully......")
                        print(f"========= successfully....")
            for folder in os.listdir(logs_path):
                files = os.path.join(logs_path, folder)
                # print(files)
                if os.path.isdir(files):
                    print(f"===Delete {folder} folder.........")
                    shutil.rmtree(folder)
                    print(f"========= successfully....")
                    # print(f"======Delete {folder} folder successfully.........")
                    number +=1

    for sfile in os.listdir(folder_path):
        folde_s = os.path.join(folder_path,sfile)
        if os.path.isdir(folde_s):
            for log in os.listdir(folde_s):
                # print(log)
                logs = os.path.join(folde_s, log)
                size = os.path.getsize(logs)
                ksize = size / 1024
                if ksize <=5:
                    print(f"===Delete file <<{logs}>> file szie: {ksize} KB successfully.........")
                    os.chdir(folde_s)
                    os.remove(logs)
                    print(f"========= delete successfully....")
                    # print(f"===============Delete file <<{logs}>> file szie: {ksize} KB successfully.........")
                    number +=1
                    print(logs)
            print(f"===========Total delete {number} files")

    for num in range(len(os.listdir(folder_path))):
        paths_dirs = os.path.join(folder_path, os.listdir(folder_path)[num])
        if os.path.isdir(paths_dirs):
            print(f"\n=== In folder <<{os.listdir(folder_path)[num]} >>")
            for j in range(len(os.listdir(paths_dirs))):
                logz = os.path.join(paths_dirs, os.listdir(paths_dirs)[j])
                print(f"======== {j +1} files {int(os.path.getsize(logz)/1024 +1)} kb  {os.listdir(paths_dirs)[j]}")




if excute_type == "R" or excute_type == "RENAME":
    rename()
elif excute_type == "D" or excute_type == "DELETE":
   delete()
else:
    print("Please input you excute type: eg: d/delete means delete or r/rename means rename:")
    exit(1)