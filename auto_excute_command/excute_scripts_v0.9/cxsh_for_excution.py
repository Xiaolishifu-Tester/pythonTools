# coding = utf-8
import csv
import os
import sys
import time
from datetime import datetime

infomation ='\nargv1 in hosts =["H0701","H0802"]  or "excute"   ;   argv2 in Schedule =["WW27","WW28","WW29","WW30","WW31","WW32","WW33"] or tcdID'
"""
argv req:
    argv1 in hosts =["H0701","H0802"]  or "excute"
    argv2 in Schedule =["WW27","WW28","WW29","WW30","WW31","WW32","WW33"] or tcdID
    
Functions:
    create log
    get all tcd 
    get all current weekend TCD
    excution command on Host
    excution single TC, need input TCD ID
"""

dirs = os.getcwd()
tcds =[]; current_weekend_tcds =[]
hosts ={"H0701":"801020","H0802":"801023"}  # dict   add ,Keys:Values
weekends =["WW27","WW28","WW29","WW30","WW31","WW32","WW33"]
log_file=""
user = "Li, DongwangX"

def write_log(message):
    '''定义log函数， 将执行过程中的步骤记录的log文档中，方便后续查看'''
    datet = datetime.now().strftime('%Y-%m-%d')
    global log_file
    log_file = "{0}_{1}_{2}_excution_{3}.log".format(get_Host, config, get_Weekend, datet)
    ctime = time.strftime("%Y-%m-%d %X", time.localtime())
    with open(log_file, 'a', encoding='utf-8') as file:
        file.write("{0}   {1}\n".format(ctime, message))


def get_all_tcds(test_file='new_command_line'):
    '''获取指定csv文件下所有的的TC, 并返回'''
    # Hosts -- weekend -- owner --  Category -- id --  title --  command
    with open(rf'{test_file}.csv', 'r') as alltcds:
        alltcd = csv.reader(alltcds)
        # print(list(alltcd))

        # write_log("Weekend: {0};               HOST: {1}".format(get_Schedule.upper(), get_Host.upper()))
        for tcd_line in list(alltcd):
            host = tcd_line[0]
            weekend = tcd_line[1]
            owner = tcd_line[2]
            category = tcd_line[3]
            id = tcd_line[4]
            title = tcd_line[5]
            cmd = tcd_line[6]
            single_tcd = [host, weekend, owner, category, id, title, cmd]
            global tcds
            tcds.append(single_tcd)
            write_log("Add CSV File Test Case:  {0}   {1}    {2}   {3}    {4}   {5}".format(weekend, owner, category, id, title, cmd))

        write_log("CSV File Total {0} tcds.\n".format(len(tcds)-1))


def get_current_weekend_tcds():
    # Hosts -- weekend -- owner --  Category -- id --  title --  command
    get_all_tcds()
    for tcd in tcds:
        if tcd[1] == get_Weekend.upper() and tcd[0] == get_Host.upper() and tcd[2] == user:
            global current_weekend_tcds
            current_weekend_tcds.append(tcd)
            write_log("Add current weekend testcase: {0} {1} {2} {3} {4} {5} ".format(tcd[0],tcd[1],tcd[2],tcd[3],tcd[4],tcd[5]))
    write_log("Current weekend total running  {0} tcds.\n".format(len(current_weekend_tcds)))


def excute_current_weekend_cmd():
    """
    get id's command and to running it
    :param cmd:
    :return:
    """
    # Hosts -- weekend --owner --  Category -- id --  title --  command
    get_current_weekend_tcds()
    for tcd in current_weekend_tcds:
        host = tcd[0]
        weekend = tcd[1]
        owner = tcd[2]
        category = tcd[3]
        id = tcd[4]
        title = tcd[5]
        cmd = tcd[6]
        write_log("===========================START===={0}=========={1}=====================================".format(host, weekend))
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
                write_log("Excute command successfully!!!")
            else:
                write_log("===================ERROR==ERROR====ERROR====================================")
                write_log("Excute command not successfully, Please check CMD")
            write_log("===========================END===================================================\n")
        else:
            write_log("Command is None, Please Check!:  Category: {0}  id: {1} title: {2} command: {3} ".format(category, id, title, cmd))
            write_log("End time:                 {0}".format(time.strftime("%Y-%m-%d %X", time.localtime())))
            etime = time.time()
            write_log("Total Used:  {0}  minutes.\n".format((etime - stime) / 60))


def excution_id_tcd(id):
    '''根据ID， 获取command line 并执行'''
    # Hosts -- weekend --owner --  Category -- id --  title --  command
    get_all_tcds()
    for tcd in tcds:
        owner = tcd[2]
        category = tcd[3]
        id = tcd[4]
        title = tcd[5]
        cmd = tcd[6]
        if get_Weekend == id:
            write_log("===========================START===================================================")
            write_log("START time:               {0}".format(time.strftime("%Y-%m-%d %X", time.localtime())))
            stime = time.time()
            if cmd:
                # Hosts -- weekend --  Category -- id --  title --  command
                write_log(
                    "START Running  Category: {0}  id: {1} title: {2} command: {3} ".format(category, id, title, cmd))
                exit_code = os.system(r'{}'.format(cmd))
                write_log("End time:                 {0}".format(time.strftime("%Y-%m-%d %X", time.localtime())))
                etime = time.time()
                write_log("Total Used:  {0}  minutes.".format((etime - stime) / 60))
                if exit_code == 0:
                    write_log("Excute command successfully!!!")
                else:
                    write_log("===================ERROR==ERROR====ERROR====================================")
                    write_log("Excute command not successfully, Please check CMD")
                write_log("===========================END===================================================\n")
            else:
                write_log(
                    "Command is None, Please Check!:  Category: {0}  id: {1} title: {2} command: {3} ".format(category, id, title, cmd))
                write_log("End time:                 {0}".format(time.strftime("%Y-%m-%d %X", time.localtime())))
                etime = time.time()
                write_log("Total Used:  {0}  minutes.\n".format((etime - stime) / 60))


if __name__ == '__main__':

    if len(sys.argv)  != 3:
        print(infomation)
    else:
        get_Weekend = sys.argv[2].lstrip("--")
        get_Host = sys.argv[1].lstrip("--")
        for keys in hosts.keys():
            if keys == get_Host:
                config = hosts.get(keys)
        if get_Host == "excute":
            write_log("run ID： {0}".format(get_Weekend))
            excution_id_tcd(get_Weekend)
        else:
            if get_Host not in hosts.keys() or get_Weekend not in weekends:
                print(infomation)
            else:
                write_log("HOST NAME: {0}:{1}      Weekend：   {2}".format(get_Host, config, get_Weekend))
                excute_current_weekend_cmd()
    print("log file in: {0}\\{1}".format(dirs, log_file))
