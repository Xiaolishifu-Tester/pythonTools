# coding = utf-8
import csv, os, sys, time
from datetime import datetime

helpInfo="""
Execute the appropriate test cases as required
Parameter description:  python cxsh_for_excution_v3.0.py  --argv1  --argv2  --argv3
    
    host: Execute the corresponding test cases on a machine-by-machine basis
    excute : Provide test case number execution to support multiple use cases
    priority: Execute the corresponding test cases according to the priority of the test cases
    
used method 1:  python cxsh_for_excution_v3.0.py --host --H0701<,H0802> --WW28<,WW29,WW30>
used method 2:  python cxsh_for_excution_v3.0.py --excute --H0701<,H0802> --id1<,id2,id3,id4>
used method 3:  python cxsh_for_excution_v3.0.py --priority --H0701<,H0802> --p1<,p2,p3,p4>

"""


TESTCASEFORMCSV = rf"testcase_running_command"
ALLHOSTS = {"H0701": "801020", "H0802": "801023", "null": "ZW", "all": "allhost"}  # dict   add ,Keys:Values
ALLWEEKENDS = ["WW27", "WW28", "WW29", "WW29RAS", "WW30", "WW30RAS", "WW31", "WW32", "WW33"]  # list
TESTER = "Li, DongwangX"  #

# Below par no need to modify
ALLTCDSFROMTESTFILE = []
NEEDTESTTCDS = []
GETARGV1 = sys.argv[1].lstrip("--") # argv1
GETHOSTS = sys.argv[2].lstrip("--").split(",") # argv2
GETTYPES = sys.argv[3].lstrip("--").split((",")) #argv3T
TYPES =["host", "excute", "priority"]
ALLPRIORITYS = {"P1", "P2", "P3", "P4"}
CURRENTDATE = datetime.now().strftime('%Y-%m-%d')
CURRENTCTIMES = time.strftime("%Y-%m-%d %X", time.localtime())
CTIMES = CURRENTCTIMES.split(" ")
CTIMES1 = CTIMES[1].split(":")
CTIME = rf"{CTIMES1[0]}_{CTIMES1[1]}_{CTIMES1[2]}"
TIMES = rf"{CTIMES[0]}_{CTIME}"
LOGGILE = rf"excute_cxsh_{'_'.join([str(item) for item in GETHOSTS]) }_{'_'.join([str(item) for item in GETTYPES])}_{TIMES}.log"


def writeLog(message):
    '''??log?????'''
    currenttimes = time.strftime("%Y-%m-%d %X", time.localtime())
    with open(LOGGILE, 'a', encoding='utf-8') as file:
        file.write("{0}   {1}\n".format(currenttimes, message))


def getAllTCDs(testfile=TESTCASEFORMCSV):
    # fileds = ['host', 'weekend', 'owner', 'category', 'priority', 'id', 'title', 'cmd']
    tcds_number = 0
    # getAllArgvs()
    with open(rf'{testfile}.csv', 'r') as alltcds:
        alltcd = csv.reader(alltcds)
        for tcd_line in list(alltcd):
            host = tcd_line[0]
            weekend = tcd_line[1]
            owner = tcd_line[2]
            category = tcd_line[3]
            priority = tcd_line[4]
            id = tcd_line[5]
            title = tcd_line[6]
            cmd = tcd_line[7]
            single_tcd = [host, weekend, owner, category, priority, id, title, cmd]
            global ALLTCDSFROMTESTFILE
            ALLTCDSFROMTESTFILE.append(single_tcd)
            tcds_number += 1
            #writeLog("Add CSV File {7} Test Case:  {0}   {1}    {2}   {3}    {4}   {5}  {6}".format(weekend, owner, category,  priority, id, title, cmd, tcds_number - 1))

        writeLog("CSV File Total {0} tcds.\n".format(len(ALLTCDSFROMTESTFILE) - 1))


def getNeedRunTCDS():
    # fileds = ['host', 'weekend', 'owner', 'category', 'priority', 'id', 'title', 'cmd']
    global NEEDTESTTCDS
    number =0
    getAllTCDs()  #????csv??????tcds
    for numi in range(len(GETHOSTS)):
        for numj in range(len(GETTYPES)):
            for tcds in ALLTCDSFROMTESTFILE:
                if GETARGV1 =="host":
                    if GETHOSTS[numi] == tcds[0] and GETTYPES[numj] == tcds[1] and tcds[2] == TESTER:
                        number +=1
                        NEEDTESTTCDS.append(tcds)
                        writeLog(
                            "Add {7} current weekend testcase: {0} {1} {2} {3} {4} {5} {6} ".format(tcds[0], tcds[1],
                                                                                                    tcds[2], tcds[3],
                                                                                                    tcds[4], tcds[5],
                                                                                                    tcds[6], number))
                elif GETARGV1.lstrip("--") =="excute":
                    # print(tcds[0], tcds[5])
                    # if GETHOSTS[numi] == "all":
                    #     number += 1
                    #     NEEDTESTTCDS.append(tcds)
                    if (GETHOSTS[numi] == tcds[0] or GETHOSTS[numi] == "all") and GETTYPES[numj] == str(tcds[5]): # and tcds[2] == TESTER:
                        number += 1
                        NEEDTESTTCDS.append(tcds)
                        writeLog(
                            "Add {7} current weekend testcase: {0} {1} {2} {3} {4} {5} {6} ".format(tcds[0], tcds[1],
                                                                                                    tcds[2], tcds[3],
                                                                                                    tcds[4], tcds[5],
                                                                                                    tcds[6], number))
                else:
                    if GETHOSTS[numi] == tcds[0] and GETTYPES[numj] == tcds[4] and tcds[2] == TESTER:
                        number += 1
                        NEEDTESTTCDS.append(tcds)
                        writeLog("Add {7} current weekend testcase: {0} {1} {2} {3} {4} {5} {6} ".format(tcds[0], tcds[1], tcds[2], tcds[3], tcds[4], tcds[5],
                                                                                tcds[6],number))
    writeLog("Current weekend total running  {0} tcds.\n".format(len(NEEDTESTTCDS)))


def excutionAllTcd(all_tcds=NEEDTESTTCDS):
    # Hosts -- weekend --owner --  Category  -- priority -- id --  title --  command
    getNeedRunTCDS()
    successfully_number = 0; error_number =0
    for tcd in all_tcds:
        host = tcd[0]
        weekend = tcd[1]
        owner = tcd[2]
        category = tcd[3]
        priority = tcd[4]
        id = tcd[5]
        title = tcd[6]
        cmd = tcd[7]
        # if GETARGV1.lstrip("--") == "excute":
        writeLog("===========================START==={0}===={1}===={2}======{3}===============================".format(weekend, priority, owner, ALLHOSTS))
        # else:
        #     writeLog("===========================START==={0}===={1}===={2}=====================================".format(host, weekend, config))
        writeLog("START time:               {0}".format(time.strftime("%Y-%m-%d %X", time.localtime())))
        stime = time.time()
        if cmd:
            # Hosts -- weekend --owner --  Category -- id --  title --  command
            writeLog("START Running  Category: {0}  id: {1} title: {2} command: {3} ".format(category, id, title, cmd))
            exit_code = os.system(r'{}'.format(cmd))
            # exit_code =1
            writeLog("End time:                 {0}".format(time.strftime("%Y-%m-%d %X", time.localtime())))
            etime = time.time()
            writeLog("Total Used:  {0}  minutes.".format((etime - stime) / 60))
            if exit_code == 0:
                successfully_number += 1
                writeLog("Excute command successfully!!!")
            else:
                error_number += 1
                writeLog("===========================ERROR====ERROR====ERROR====================================")
                writeLog("Total {0} tcds excute command not successfully, Please check!!!".format(error_number))
            writeLog("=================================END===================================================")
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
    writeLog(f"Your input : python {sys.argv[0]} --{GETARGV1} --{GETHOSTS} --{GETTYPES}")
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
            # writeLog(f"{helpInfo}\n")
        writeLog(f"all host config : {ALLHOSTS}\n")
        excutionAllTcd()
        # print(NEEDTESTTCDS)
        # print(len(NEEDTESTTCDS))


