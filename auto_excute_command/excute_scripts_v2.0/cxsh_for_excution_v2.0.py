# coding = utf-8
import csv, os, sys, time
from datetime import datetime

infomation = '\nargv1 in hosts =["H0701","H0802"]  or "excute"  or "prioritys"   ;   argv2 in Schedule =["WW27","WW28","WW29","WW30","WW31","WW32","WW33"] or "tcdID,tcdID"  or "P*'
"""
argv req:
    argv1 in hosts =["H0701","H0802"]  or "--excute" or "prioritys"
    argv2 in Schedule =["WW27","WW28","WW29","WW29RAS","WW30","WW30RAS","WW31","WW32","WW33"] or "--tcdID,tcdID" or "P*"

Functions:
    create log
    get all tcd 
    get all current weekend TCD
    excution command on Host
    excution single TC, need input TCD ID
"""

testfile = 'testcase_command'
dirs = os.getcwd()
tcds = [];
current_weekend_tcds = []
# hosts is a dict
hosts = {"H0701": "801020", "H0802": "801023"}  # dict   add ,Keys:Values
all_prioritys = {"P1", "P2", "P3", "P4"}
weekends = [ "WW27", "WW28", "WW29", "WW29RAS", "WW30", "WW30RAS", "WW31", "WW32", "WW33"]  # list
user = "Li, DongwangX"  # str
datet = datetime.now().strftime('%Y-%m-%d')


def write_log(message):
    ctime = time.strftime("%Y-%m-%d %X", time.localtime())
    with open(log_file, 'a', encoding='utf-8') as file:
        file.write("{0}   {1}\n".format(ctime, message))


def get_all_tcds(test_file=testfile):
    # fileds = ['host', 'weekend', 'owner', 'category', 'priority', 'id', 'title', 'cmd']
    tcds_number =0
    with open(rf'{test_file}.csv', 'r') as alltcds:
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
            global tcds
            tcds.append(single_tcd)
            tcds_number +=1
            write_log(
                "Add CSV File {7} Test Case:  {0}   {1}    {2}   {3}    {4}   {5}  {6}".format(weekend, owner, category, priority, id,
                                                                                      title, cmd, tcds_number-1))

        write_log("CSV File Total {0} tcds.\n".format(len(tcds) - 1))


def get_current_weekend_tcds():
    # ['host', 'weekend', 'owner', 'category', 'priority', 'id', 'title', 'cmd']
    get_all_tcds()
    for tcd in tcds:
        # print("\n",tcd[1], tcd[0], tcd[2])
        # print(get_Weekend.upper(), get_Host.upper(), user)
        if tcd[1] == get_Weekend.upper() and tcd[0] == get_Host.upper() and tcd[2] == user:
            global current_weekend_tcds
            current_weekend_tcds.append(tcd)
            write_log(
                "Add current weekend testcase: {0} {1} {2} {3} {4} {5} {6} ".format(tcd[0], tcd[1], tcd[2], tcd[3], tcd[4], tcd[5],
                                                                                tcd[6]))
    write_log("Current weekend total running  {0} tcds.\n".format(len(current_weekend_tcds)))


def get_excute_id(ids):
    # fileds = ['host', 'weekend', 'owner', 'category', 'priority', 'id', 'title', 'cmd']
    get_all_tcds()
    ex_ids = ids.split("-")
    # print(ex_ids)
    for i in range(len(ex_ids)):
        single_id = ex_ids[i]
        for j in range(len(tcds)):
            host =tcds[j][0]
            weekend = tcds[j][1]
            owner = tcds[j][2]
            category = tcds[j][3]
            priority = tcds[j][4]
            id = tcds[j][5]
            title = tcds[j][6]
            cmd = tcds[j][7]
            if single_id == id:
                single_tc= [host, weekend, owner, category, priority, id, title, cmd]
                current_weekend_tcds.append(single_tc)
                write_log(
                    "Add {0} testcase: {1} {2} {3} {4} {5} {6} {7} ".format(host, weekend, owner, category, priority, id, title, cmd))
        print("Can't find ID:{0}".format(single_id))


def get_priority_tcds(priority):
    number =0
    get_all_tcds()
    all_priority = priority.split("-")
    write_log("GET: HOST: {1} Priority: {0} USER: {2} all test case ".format(get_Weekend, get_pHost, user))
    for p_num in range(len(all_priority)):
        get_priority = all_priority[p_num]
        # ['host', 'weekend', 'owner', 'category', 'priority', 'id', 'title', 'cmd']
        for num in range(len(tcds)):
            tc_priority = tcds[num][4]
            tc_owner = tcds[num][2]
            tc_host = tcds[num][0]
            # print(tc_priority, get_priority, tc_owner, user, tc_host, get_pHost)
            if tc_priority == get_priority and tc_owner == user and tc_host == get_pHost:
                global  current_weekend_tcds
                current_weekend_tcds.append(tcds[num])
                number +=1
                write_log(
                    "Add {8} current priority:{7} testcase: {0} {1} {2} {3} {4} {5} {6} ".format(tcds[num][0], tcds[num][1], tcds[num][2],
                                                                                             tcds[num][3],
                                                                                             tcds[num][5], tcds[num][6],
                                                                                             tcds[num][7], tcds[num][4],number))
    write_log("{0} total need running {1} tcds".format(all_priority, number))


def excution_id_tcd(all_tcds):
    # Hosts -- weekend --owner --  Category  -- priority -- id --  title --  command
    successfully_number = 0; error_number =0
    for tcd in all_tcds:
        host = tcd[0]
        if get_pHost in hosts:
            config = hosts.get(get_pHost)
        weekend = tcd[1]
        owner = tcd[2]
        category = tcd[3]
        priority = tcd[4]
        id = tcd[5]
        title = tcd[6]
        cmd = tcd[7]
        if get_Host == "excute":
            write_log("===========================START==={0}===={1}===={2}=====================================".format(get_pHost, weekend, config))
        else:
            write_log("===========================START==={0}===={1}===={2}=====================================".format(host, weekend, config))
        write_log("START time:               {0}".format(time.strftime("%Y-%m-%d %X", time.localtime())))
        stime = time.time()
        if cmd:
            # Hosts -- weekend --owner --  Category -- id --  title --  command
            write_log("START Running  Category: {0}  id: {1} title: {2} command: {3} ".format(category, id, title, cmd))
            exit_code = os.system(r'{}'.format(cmd))
            write_log("End time:                 {0}".format(time.strftime("%Y-%m-%d %X", time.localtime())))
            etime = time.time()
            write_log("Total Used:  {0}  minutes.".format((etime - stime) / 60))
            if exit_code == 0:
                successfully_number += 1
                write_log("Excute command successfully!!!")
            else:
                error_number += 1
                write_log("===========================ERROR====ERROR====ERROR====================================")
                write_log("Total {0} tcds excute command not successfully, Please check!!!".format(error_number))
            write_log("=================================END===================================================")
        else:
            error_number +=1
            write_log(
                "Command is None, Please Check!:  Category: {0}  id: {1} title: {2} command: {3} ".format(category, id,
                                                                                                          title, cmd))
            write_log("End time:                 {0}".format(time.strftime("%Y-%m-%d %X", time.localtime())))
            etime = time.time()
            write_log("Total Used:  {0}  minutes.\n".format((etime - stime) / 60))
        write_log(
            "total runing successfully {0} tcds and total running {1} tcds appear some error\n".format(successfully_number, error_number))


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print(infomation)
    else:
        get_Weekend = sys.argv[2].lstrip("--")
        get_Host = sys.argv[1].lstrip("--")
        get_pHost = sys.argv[3].lstrip("--")
        log_file = "{0}{1}_excution_{2}.log".format(get_Host, sys.argv[2], datet)
        if get_Host == "priority":
            if get_pHost in hosts.keys():
                config = hosts.get(get_pHost)
            print("{2} running : {0} is {1} ".format(sys.argv[1], sys.argv[2], sys.argv[2]))
            write_log("GET: {0} all test case ".format(get_Weekend))
            get_priority_tcds(get_Weekend)

        elif get_Host == "excute":
            # print("ON Host {0} ID= {1}  test case".format(sys.argv[1], sys.argv[2]))
            # all_tcds = get_Weekend
            print("Op type: {0} run ID: {1}".format(sys.argv[1], sys.argv[2]))
            write_log("running ID: {0}".format(get_Weekend))
            get_excute_id(get_Weekend)
        else:
            if get_Host in hosts.keys():
                config = hosts.get(get_Host)
                write_log("HOST NAME: {0}:{1}      Weekend:  {2}".format(get_Host, config, get_Weekend))
                print("get Host: {0}  weekend: {1} all test case".format(sys.argv[1], sys.argv[2]))
                get_current_weekend_tcds()
            else:
                print(infomation)
        excution_id_tcd(current_weekend_tcds)


