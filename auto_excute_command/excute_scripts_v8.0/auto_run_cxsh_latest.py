# coding = utf-8
import csv, os, sys, time, re
from datetime import datetime
import pandas as pd  # pandas>=2.0.2（2.0.2/2.2.2）
import shutil, socket

helpInfo = f"""
Execute the appropriate test cases as required
Parameter description:  python {sys.argv[0]}  --argv1  --argv2  --argv3

    host: Execute the corresponding test cases on a machine-by-machine basis
    excute : Provide test case number execution to support multiple use cases
    priority: Execute the corresponding test cases according to the priority of the test cases

used method 1:  python {sys.argv[0]} --host --H0701<,H0802,all> --WW28<,WW29,WW30>
used method 2:  python {sys.argv[0]} --excute --H0701<,H0802,all> --id1<,id2,id3,id4>
used method 3:  python {sys.argv[0]} --priority --H0701<,H0802,all> --p1<,p2,p3,p4>
test env    4：  python {sys.argv[0]} --excute --all --118119120

"""
# Need to modify
schedule_file = r"CXSH SPR4800 with DDR5-5600DIMM Dry Run Report"  # 只需要复制原始表格的名称， 不要复制加了schedule字段的名称
ALLHOSTS = {"H0502": "803765","all":"11811912012"} # dict   add ,Keys:Values --> keys:机器名称 Values: onecloud systemID
SCRIPTSTYPE = 1  # 1 --> cxsh bifrost   2 --> dtaf_connect  3 -->bifrost
if SCRIPTSTYPE == 1:
    SCRIPTSDIR = rf"C:\CXSH\bifrost\bifrost\release"  # 测试脚本的路径
    autologpath = rf"C:\temp\test_logs"
elif SCRIPTSTYPE == 2:
    SCRIPTSDIR = rf"C:\DPG_Automation\dtaf_content"
    autologpath = rf"C:\automation\dtaf_logs"
elif SCRIPTSTYPE == 3:
    SCRIPTSDIR = rf"C:\bifrost\release"  # 测试脚本的路径
    autologpath = rf"C:\temp\test_logs"


# Below par no need to modify
ALLTCDSFROMTESTFILE = []
NEEDTESTTCDS = []
test_result = []
try:
    GETARGV1 = sys.argv[1].lstrip("--").lower()  # argv1
    GETHOSTS = sys.argv[2].lstrip("--").split(",")  # argv2
    GETTYPES = sys.argv[3].lstrip("--").split((","))  # argv3T
except Exception as e:
    print(helpInfo, e)
TYPES = ["host", "h","e","p","excute", "priority"]  # 都为小写， 不用改
TIMES = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d-%H-%M-%S')
TCEXCELDIR= os.getcwd()  # LOGDIR = rf"C:\Users\General\Desktop\IPU\excute_cmd"  # C:\Users\General\Desktop\IPU\excute_cmd   C:\temp\test_logs  C:\PY\IPU\CXSH\excute_scripts_v4.0\test
LOGGILE = rf"logfile_descriptions_{GETARGV1}_{TIMES}.log"
test_result_excel = rf"test_result_{GETARGV1}_{TIMES}.xlsx"
TESTCASEFORMEXCEL = rf"{schedule_file}_schedule.xlsx"
hostname = socket.getfqdn().upper()
folder_path = fr"{TCEXCELDIR}\{TIMES}"
if not os.path.exists(folder_path):
    os.makedirs(folder_path)
folder_list =[]; folder_time = []


def writeLog(message):
    currenttimes = time.strftime("%Y-%m-%d %X", time.localtime())
    os.chdir(folder_path)
    with open(LOGGILE, 'a', encoding='utf-8') as file:
        file.write("{0}   {1}\n".format(currenttimes, message))


def getAllTCDs(testfile=TESTCASEFORMEXCEL,sheet_name ="Sheet1"):
    # fileds = ['host', 'weekend', 'owner', 'category', 'priority', 'id', 'title', 'cmd']
    os.chdir(TCEXCELDIR)
    data_form = pd.read_excel((testfile), sheet_name=sheet_name)
    global ALLTCDSFROMTESTFILE
    for num in range(len(list(data_form.index.values))):
        ALLTCDSFROMTESTFILE.append(list(data_form.loc[num].values))
    writeLog(f"Total {len(ALLTCDSFROMTESTFILE)} tcds from schedule excel\n")


def getNeedRunTCDS():
    # fileds = ['host', 'weekend', 'owner', 'category', 'priority', 'id', 'title', 'cmd']
    global NEEDTESTTCDS
    number =0
    getAllTCDs()  # from excel    print(GETHOSTS)
    for numi in range(len(GETHOSTS)):
        for numj in range(len(GETTYPES)):
            for tcds in ALLTCDSFROMTESTFILE:
                if GETARGV1 =="host" or GETARGV1 == "h":
                    # print(GETTYPES[numj].upper())
                    # print("tcds",str(tcds[1]).upper())
                    if GETHOSTS[numi].lower() == "all":
                        if GETTYPES[numj].upper() == str(tcds[1]).upper(): # and tcds[2] == TESTER:
                            number +=1
                            NEEDTESTTCDS.append(tcds)
                            writeLog("Add {7} current weekend testcase: {0} {1} {2} {3} {4} {5} {6} ".format(tcds[0], tcds[1], tcds[2], tcds[3], tcds[4], tcds[5], tcds[6],number))
                    else:
                        if GETHOSTS[numi].upper() == str(tcds[0]).upper() and GETTYPES[numj].upper() == str(tcds[1]).upper(): # and tcds[2] == TESTER:
                            number +=1
                            NEEDTESTTCDS.append(tcds)
                            writeLog("Add {7} current weekend testcase: {0} {1} {2} {3} {4} {5} {6} ".format(tcds[0], tcds[1], tcds[2], tcds[3], tcds[4], tcds[5], tcds[6],number))
                elif GETARGV1 =="excute" or GETARGV1 == "e":
                    if GETHOSTS[numi].lower() == "all":
                        if GETTYPES[numj].upper() == str(tcds[5]).upper():
                            number += 1
                            NEEDTESTTCDS.append(tcds)
                            writeLog("Add {7} current weekend testcase: {0} {1} {2} {3} {4} {5} {6} ".format(tcds[0], tcds[1], tcds[2], tcds[3], tcds[4], tcds[5], tcds[6],number))
                        # else:
                        #     print(f"{numj} can't find , please check to it")
                    else:
                        if GETHOSTS[numi].upper() == str(tcds[0]).upper() and GETTYPES[numj].upper() == str(tcds[5]).upper(): # and tcds[2] == TESTER:
                            number += 1
                            NEEDTESTTCDS.append(tcds)
                            writeLog("Add {7} current weekend testcase: {0} {1} {2} {3} {4} {5} {6} ".format(tcds[0], tcds[1], tcds[2], tcds[3], tcds[4], tcds[5], tcds[6],number))
                elif GETARGV1 =="priority" or GETARGV1 == "p":
                    if GETHOSTS[numi].lower() =="all":
                        if GETTYPES[numj].upper() == str(tcds[4]).upper():
                            number += 1
                            NEEDTESTTCDS.append(tcds)
                            writeLog("Add {7} current weekend testcase: {0} {1} {2} {3} {4} {5} {6} ".format(tcds[0], tcds[1], tcds[2], tcds[3], tcds[4], tcds[5], tcds[6],number))

                    else:
                        if GETHOSTS[numi].upper() == str(tcds[0]).upper() and GETTYPES[numj].upper() == str(tcds[4]).upper(): # and tcds[2] == TESTER:
                            number += 1
                            NEEDTESTTCDS.append(tcds)
                            writeLog("Add {7} current weekend testcase: {0} {1} {2} {3} {4} {5} {6} ".format(tcds[0], tcds[1], tcds[2], tcds[3], tcds[4], tcds[5], tcds[6],number))
                else:
                    print("input error")
                    exit(1)
    writeLog("Current weekend total running  {0} tcds.\n".format(len(NEEDTESTTCDS)))


def excutionAllTcd(all_tcds=NEEDTESTTCDS):
    # Hosts -- weekend --owner --  Category  -- priority -- id --  title --  command
    getNeedRunTCDS()
    successfully_number = 0; error_number =0
    # log_folder_name =""
    excel_head = pd.DataFrame(
        {'TEST_TIME': [], 'RESULT': [],'ID': [], 'HOSTNAME': [],'TITLE': [],'LOG_FOLDER_NAME': [],  'DURATION': [],'HOST_CONFIG': [], 'HOST':[],'WEEKEND': [], 'OWNER': [],
         'CATEGORY': [],
         'PRIORITY': [],
         'CMD': []})
    excel_head.to_excel(test_result_excel, header=True, index=False)
    for tcd in all_tcds:
        # time.sleep(300)
        host = f"H{hostname[11:15]}"
        weekend = tcd[1]
        owner = tcd[2]
        category = tcd[3]
        priority = tcd[4]
        id = tcd[5]
        title = tcd[6]
        cmd = tcd[7]
        host_key = ALLHOSTS.get(f"{host}")
        writeLog("===========================START==={0}===={1}===={2}======{3}:{4}===============================".format(weekend, priority, owner, host, host_key))
        writeLog("START time:               {0}".format(time.strftime("%Y-%m-%d %X", time.localtime())))
        stime = time.time()
        if cmd:
            # Hosts -- weekend --owner --  Category -- id --  title --  command
            writeLog("START Running:  \nHost:  {4}  \nCategory: {0}  \nid: {1} \ntitle: {2} \ncommand: {3} ".format(category, id, title, cmd, hostname))
            os.chdir(SCRIPTSDIR)
            if SCRIPTSTYPE == 1 or SCRIPTSTYPE == 3: # bifrost
                currenttimes = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d-%H-%M-%S')
                exit_code = os.system(r'{}'.format(cmd))
            elif SCRIPTSTYPE == 2: # dtaf_content
                currenttimes =datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H.%M.%S')
                exit_code = os.system(r'python {}'.format(cmd))
            writeLog("End time:                 {0}".format(time.strftime("%Y-%m-%d %X", time.localtime())))
            etime = time.time() - 13
            times_s = etime -stime
            times = times_s/60
            writeLog("Total Used:  {0}  minutes.".format(times))
            if exit_code == 0:
                successfully_number += 1
                test_result = "PASS"
                writeLog(f"Excute {id}: {title} command successfully!!!")
            else:
                error_number += 1
                test_result = "FAIL"
                writeLog("===========================ERROR====ERROR====ERROR====================================")
                writeLog(f"Excute {id} command Fail, Please check it!!!!!!!")
                writeLog("Total {0} tcds excute command not successfully, Please check!!!".format(error_number))
            writeLog("=================================END===================================================")
            writeLog(f"======================TEST RESULT:  {test_result}=============================================")
            # time.sleep(10)
            log_folder_name = rf"{title}_{currenttimes[:-2]}*_{test_result}"
            writeLog(f"Start copy test case <<{title}>> logs to {folder_path}")
            currenttimes_minutes = currenttimes[:-2]
            patterns = f".*{currenttimes_minutes}.*"
            writeLog(f"cd {autologpath} successfully.....")
            os.chdir(autologpath)
            folder_file = os.listdir()
            # test_flag = True
            for file in folder_file:
                if re.match(patterns, file):
                    writeLog(rf"patterns <<{file}>> tcd folder in {autologpath}")
                    writeLog(fr"Start copy test case {autologpath}\{file} logs to {folder_path}")
                    os.chdir(autologpath)
                    # tc_title = file[:-25]
                    if SCRIPTSTYPE == 1 or SCRIPTSTYPE == 3: # bifrost
                        tc_date = file[-24:-5]
                        tc_result = file[-4:]
                    elif SCRIPTSTYPE == 2: # dtaf_content
                        tc_date = file[-19:]
                        tc_result = test_result
                    source_path = os.path.join(autologpath, file)
                    destination_path = os.path.join(folder_path, file)
                    # 脚本生成的log copy到指定的文件夹, 文件夹根据脚本只从的日期自动生成
                    if os.path.isdir(source_path):
                        try:
                            shutil.copytree(source_path, destination_path)
                            writeLog(f"Copy {source_path} file to {folder_path} successfully!!!")
                            rename_title = f"{id}_{title}_{tc_date}_{tc_result}"
                            writeLog(f"cd {folder_path} successfully!!!!!!!!!!!")
                            writeLog(f"Start rename <<{file}>>  to  <<{rename_title}>>")
                            os.chdir(folder_path)
                            try:
                                # 根据log生成的时间和结果， TC的title对log文件夹重新命名， 命名规则：ID_title_logdate_result
                                os.rename(file, rename_title)
                                writeLog(f"Rename <<{title}>> to  <<{rename_title}>>   successfully")
                            except FileExistsError as e:
                                os.rename(file, rename_title + "_2")
                                writeLog(f"File name exist!!! error= {e}")
                            except FileNotFoundError as f:
                                writeLog(f"File not found!!!error={f} \n  <<{file}>>")
                            except BaseException as g:
                                writeLog(f"other error =={g}")
                        except FileExistsError as e:
                            writeLog(f"File Exist {e}")
                            writeLog(f"SKIP   copy and SKIP rename  <<{file}>> folder to {folder_path}!!!")
            os.chdir(folder_path)
            # 将测试的结果写入excel表格里。
            df = pd.DataFrame({'TEST_TIME': [currenttimes], 'RESULT': [test_result],'ID': [id], 'HOSTNAME': [hostname],'TITLE': [title],'LOG_FOLDER_NAME': [log_folder_name],'DURATION': [int(times+1)],'HOST_CONFIG':[host_key],'HOST': [f"{host}"],'WEEKEND': [weekend], 'OWNER': [owner],
                               'CATEGORY': [category], 'PRIORITY': [priority], 'CMD': [cmd]})
            with pd.ExcelWriter(test_result_excel, engine="openpyxl", mode="a", if_sheet_exists="overlay") as writer:
                df.to_excel(writer, sheet_name="Sheet1", startrow=writer.sheets['Sheet1'].max_row, header=False,
                            index=False)
            writeLog(f"Runninng {error_number + successfully_number} tcds result to {test_result_excel} successfully")

        else:
            error_number +=1
            writeLog(
                "Command is None, Please Check!:  Category: {0}  id: {1} title: {2} command: {3} ".format(category, id,
                                                                                                          title, cmd))
            writeLog("End time:                 {0}".format(time.strftime("%Y-%m-%d %X", time.localtime())))
            etime = time.time()
            writeLog("Total Used:  {0}  minutes.\n".format((etime - stime) / 60))
        writeLog(
            "============================SUCCCESSFULLY:  {0} ============================FAIL ERROR:  {1}============================== \n".format(successfully_number, error_number))
        time.sleep(10)
        # print(time.time())

# if __name__ == '__main__':
try:
    writeLog(f"Your input : python {sys.argv[0]} {sys.argv[1]} {sys.argv[2]} {sys.argv[3]}")
except Exception as e:
    print(e)
if len(sys.argv) !=4 or GETARGV1.lower() == "help":
    print(helpInfo)
    writeLog(f"Parameter, see {helpInfo}")
else:
    # # print(ALLHOSTS.keys())
    if GETARGV1 not in TYPES:
        writeLog(f"ARGV1 input error! please see :\n{helpInfo}")
        exit(1)
    for num in range(len(GETHOSTS)):
        GETHOST=[]
        GETHOST.append(GETHOSTS[num].upper())
    for num in range(len(GETHOSTS)):
        if GETHOSTS[num].upper() not in GETHOST:
            writeLog(f"Host name input error, please check!!! \n{helpInfo}")
            exit(1)
    writeLog(f"All host config : {ALLHOSTS}\n")
    excutionAllTcd()
    writeLog(f"Test Result see: {os.path.join(os.getcwd(),test_result_excel)}")
