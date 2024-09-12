# coding = utf-8
import csv, os, sys, time
from datetime import datetime
import pandas as pd
# import logging_core #416 class LoggingManager(object):
# import framework_execution
# from tester_instrument import tester_core

helpInfo = """
Execute the appropriate test cases as required
Parameter description:  python startCXSH_excel_v5.0.py  --argv1  --argv2  --argv3

    host: Execute the corresponding test cases on a machine-by-machine basis
    excute : Provide test case number execution to support multiple use cases
    priority: Execute the corresponding test cases according to the priority of the test cases

used method 1:  python startCXSH_excel_v5.0.py --host --H0701<,H0802> --WW28<,WW29,WW30>
used method 2:  python startCXSH_excel_v5.0.py --excute --H0701<,H0802> --id1<,id2,id3,id4>
used method 3:  python startCXSH_excel_v5.0.py --priority --H0701<,H0802> --p1<,p2,p3,p4>
TEST ENV 4：    python startCXSH_excel_v5.0.py --excute --all --118119120

"""

TESTCASEFORMEXCEL = r"testcase_running_command.xlsx"
sheet_name = rf"Sheet1"
ALLHOSTS = {"H0701": "801020", "H0802": "801023", "all":"118"}  # dict   add ,Keys:Values
# ALLWEEKENDS = ["WW27", "WW28", "WW29", "WW29RAS", "WW30", "WW30RAS", "WW31", "WW32", "WW33"]  # list

# Below par no need to modify
ALLTCDSFROMTESTFILE = []
NEEDTESTTCDS = []
GETARGV1 = sys.argv[1].lstrip("--")  # argv1
GETHOSTS = sys.argv[2].lstrip("--").split(",")  # argv2
GETTYPES = sys.argv[3].lstrip("--").split((","))  # argv3T
TYPES = ["host", "excute", "priority"]
ALLPRIORITYS = {"P1", "P2", "P3", "P4"}
# CURRENTDATE = datetime.now().strftime('%Y-%m-%d')
CURRENTCTIMES = time.strftime("%Y-%m-%d %X", time.localtime())
CTIMES = CURRENTCTIMES.split(" ")
CTIMES1 = CTIMES[1].split(":")
CTIME = rf"{CTIMES1[0]}_{CTIMES1[1]}_{CTIMES1[2]}"
TIMES = rf"{CTIMES[0]}_{CTIME}"
TCEXCELDIR= os.getcwd()  # LOGDIR = rf"C:\Users\General\Desktop\IPU\excute_cmd"  # C:\Users\General\Desktop\IPU\excute_cmd   C:\temp\test_logs  C:\PY\IPU\CXSH\excute_scripts_v4.0\test
LOGGILE = rf"logfile_descriptions_{GETARGV1}_{TIMES}.log"
SCRIPTSDIR = rf"C:\CXSH\bifrost\bifrost\release"   # C:\CXSH\bifrost\bifrost\release  C:\PY\IPU\CXSH\excute_scripts_v4.0\test\test_s
if not os.path.exists(SCRIPTSDIR):
    SCRIPTSDIR = rf"C:\PY\IPU\CXSH"
test_result_excel = rf"test_result_{GETARGV1}_{TIMES}.xlsx"
date_folder = datetime.now().date()
folder_path = fr"{TCEXCELDIR}\{date_folder}"


def __doc__():
    "Enter the executed test cases into the specified file, and record the test results and the duration"
    pass
def create_folder():
    # date_folder =  datetime.now().date()
    # folder_path = fr"{LOGDIR}\{date_folder}"
    # print(folder_path)
    if not os.path.exists(fr"{TCEXCELDIR}\{date_folder}"):
        print(f"create log folder {folder_path}")
        os.makedirs(folder_path)

    return folder_path


def writeLog(message):
    '''??log?????'''
    currenttimes = time.strftime("%Y-%m-%d %X", time.localtime())
    # time.sleep(3)
    os.chdir(create_folder())
    # print(LOGDIR)
    # print(os.getcwd())
    with open(LOGGILE, 'a', encoding='utf-8') as file:
        file.write("{0}   {1}\n".format(currenttimes, message))


def getAllTCDs(testfile=TESTCASEFORMEXCEL):
    # fileds = ['host', 'weekend', 'owner', 'category', 'priority', 'id', 'title', 'cmd']
    os.chdir(TCEXCELDIR)
    data_form = pd.read_excel((TESTCASEFORMEXCEL), sheet_name=sheet_name)
    global ALLTCDSFROMTESTFILE
    for num in range(len(list(data_form.index.values))):
        ALLTCDSFROMTESTFILE.append(list(data_form.loc[num].values))
    writeLog(f"Total {len(ALLTCDSFROMTESTFILE)} tcds from schedule excel\n")


def getNeedRunTCDS():
    # fileds = ['host', 'weekend', 'owner', 'category', 'priority', 'id', 'title', 'cmd']
    global NEEDTESTTCDS
    number =0
    getAllTCDs()  # from excel    print(GETHOSTS)
    # print(GETTYPES)
    for numi in range(len(GETHOSTS)):
        for numj in range(len(GETTYPES)):
            for tcds in ALLTCDSFROMTESTFILE:
                if GETARGV1 =="host":
                    if GETHOSTS[numi] == "all":
                        if GETTYPES[numj] == tcds[1]: # and tcds[2] == TESTER:
                            number +=1
                            NEEDTESTTCDS.append(tcds)
                            writeLog("Add {7} current weekend testcase: {0} {1} {2} {3} {4} {5} {6} ".format(tcds[0], tcds[1], tcds[2], tcds[3], tcds[4], tcds[5], tcds[6],number))
                    else:
                        if GETHOSTS[numi] == tcds[0] and GETTYPES[numj] == tcds[1]: # and tcds[2] == TESTER:
                            number +=1
                            NEEDTESTTCDS.append(tcds)
                            writeLog("Add {7} current weekend testcase: {0} {1} {2} {3} {4} {5} {6} ".format(tcds[0], tcds[1], tcds[2], tcds[3], tcds[4], tcds[5], tcds[6],number))
                elif GETARGV1 =="excute":
                    if GETHOSTS[numi] == "all":
                        if GETTYPES[numj] == str(tcds[5]):
                            number += 1
                            NEEDTESTTCDS.append(tcds)
                            writeLog("Add {7} current weekend testcase: {0} {1} {2} {3} {4} {5} {6} ".format(tcds[0], tcds[1], tcds[2], tcds[3], tcds[4], tcds[5], tcds[6],number))
                    else:
                        if GETHOSTS[numi] == tcds[0] and GETTYPES[numj] == str(tcds[5]): # and tcds[2] == TESTER:
                            number += 1
                            NEEDTESTTCDS.append(tcds)
                            writeLog("Add {7} current weekend testcase: {0} {1} {2} {3} {4} {5} {6} ".format(tcds[0], tcds[1], tcds[2], tcds[3], tcds[4], tcds[5], tcds[6],number))
                else:
                    if GETHOSTS[numi] =="all":
                        if GETTYPES[numj].upper() == tcds[4]:
                            number += 1
                            NEEDTESTTCDS.append(tcds)
                            writeLog("Add {7} current weekend testcase: {0} {1} {2} {3} {4} {5} {6} ".format(tcds[0], tcds[1], tcds[2], tcds[3], tcds[4], tcds[5], tcds[6],number))

                    else:
                        if GETHOSTS[numi] == tcds[0] and GETTYPES[numj].upper() == tcds[4]: # and tcds[2] == TESTER:
                            number += 1
                            NEEDTESTTCDS.append(tcds)
                            writeLog("Add {7} current weekend testcase: {0} {1} {2} {3} {4} {5} {6} ".format(tcds[0], tcds[1], tcds[2], tcds[3], tcds[4], tcds[5], tcds[6],number))
    writeLog("Current weekend total running  {0} tcds.\n".format(len(NEEDTESTTCDS)))


def excutionAllTcd(all_tcds=NEEDTESTTCDS):
    # Hosts -- weekend --owner --  Category  -- priority -- id --  title --  command
    getNeedRunTCDS()
    successfully_number = 0; error_number =0
    excel_head = pd.DataFrame(
        {'date': [], 'result': [],'id': [], 'full_log_name': [],'title': [], 'autral_duration': [], 'duration': [],'test_config': [], 'host':[],'weekend': [], 'owner': [],
         'category': [],
         'priority': [],
         'cmd': []})
    excel_head.to_excel(test_result_excel, header=True, index=False)
    for tcd in all_tcds:
        host = tcd[0]
        weekend = tcd[1]
        owner = tcd[2]
        category = tcd[3]
        priority = tcd[4]
        id = tcd[5]
        title = tcd[6]
        cmd = tcd[7]
        host_key = ALLHOSTS.get(host)
        # if GETARGV1.lstrip("--") == "excute":
        writeLog("===========================START==={0}===={1}===={2}======{3}===============================".format(weekend, priority, owner, ALLHOSTS))
        # else:
        #     writeLog("===========================START==={0}===={1}===={2}=====================================".format(host, weekend, config))
        writeLog("START time:               {0}".format(time.strftime("%Y-%m-%d %X", time.localtime())))
        stime = time.time()
        if cmd:
            # Hosts -- weekend --owner --  Category -- id --  title --  command
            writeLog("START Running:  \nCategory: {0}  \nid: {1} \ntitle: {2} \ncommand: {3} ".format(category, id, title, cmd))
            os.chdir(SCRIPTSDIR)
            currenttimes = time.strftime("%Y-%m-%d %X", time.localtime())
            exit_code = os.system(r'{}'.format(cmd))
            # log_full_dirname = tester_core.TestLogger.log_pretest_header()
            log_full_dirname = "Not Enable"
            # exit_code =1
            writeLog("End time:                 {0}".format(time.strftime("%Y-%m-%d %X", time.localtime())))
            etime = time.time()
            times_s = etime -stime
            # times_s = framework_execution.FMWK_ExecutionManager.run_timer.current
            times = times_s/60
            writeLog("Total Used:  {0}  minutes.".format(times))
            if exit_code == 0:
                successfully_number += 1
                test_result = "PASS"
                writeLog("Excute command successfully!!!")
            else:
                error_number += 1
                test_result = "FAIL"
                writeLog("===========================ERROR====ERROR====ERROR====================================")
                writeLog("Total {0} tcds excute command not successfully, Please check!!!".format(error_number))
            writeLog("=================================END===================================================")
            writeLog(f"======================TEST RESULT:  {test_result}=============================================")
            # host_key = ALLHOSTS.get(host)
            df = pd.DataFrame({'date': [currenttimes], 'result': [test_result],'id': [id], 'full_log_name': [log_full_dirname],'title': [title],'autral_duration':[times],'duration': [int(times+1)],'test_config':[host_key],'host': [host],'weekend': [weekend], 'owner': [owner],
                               'category': [category], 'priority': [priority], 'cmd': [cmd]})
            with pd.ExcelWriter(test_result_excel, engine="openpyxl", mode="a", if_sheet_exists="overlay") as writer:
                df.to_excel(writer, sheet_name="Sheet1", startrow=writer.sheets['Sheet1'].max_row, header=False,
                            index=False)
            writeLog(f"runninng {error_number + successfully_number} tcds result to {test_result_excel} successfully")

        else:
            error_number +=1
            writeLog(
                "Command is None, Please Check!:  Category: {0}  id: {1} title: {2} command: {3} ".format(category, id,
                                                                                                          title, cmd))
            writeLog("End time:                 {0}".format(time.strftime("%Y-%m-%d %X", time.localtime())))
            etime = time.time()
            writeLog("Total Used:  {0}  minutes.\n".format((etime - stime) / 60))
        writeLog(
            "total runing successfully {0} tcds and total running {1} tcds appear some error\n".format(successfully_number, error_number))


if __name__ == '__main__':
    writeLog(f"Your input : python {sys.argv[0]} {sys.argv[1]} {sys.argv[2]} {sys.argv[3]}")
    if len(sys.argv) !=4:
        writeLog(f"Parameter, see {helpInfo}")
    else:
        # print(ALLHOSTS.keys())
        if GETARGV1 not in TYPES:
            writeLog(f"ARGV1 input error! please see :\n{helpInfo}")
            exit(1)
        for num in range(len(GETHOSTS)):
            if GETHOSTS[num] not in ALLHOSTS.keys():
                writeLog(f"host name input error, please check!!! \n{helpInfo}")
                exit(1)
            # else:
            #     host_key = ALLHOSTS.get(GETHOSTS[num])
            #     print(host_key)
            # writeLog(f"{helpInfo}\n")
        writeLog(f"all host config : {ALLHOSTS}\n")
        excutionAllTcd()
        # print(NEEDTESTTCDS)
        # print(len(NEEDTESTTCDS))
