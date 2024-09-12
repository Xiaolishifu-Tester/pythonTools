# coding=utf-8
import csv
import os
import sys
import time
from datetime import datetime

# dirs = os.getcwd()
all_ids=[]; have_ids=[]
log_file=""
host1 ="H0701"; host2 = "H0802"
schedule_testcase_format = """0 ID, 1 Title,2 Category, 3 Priority,4 A:1DPC,5  Schedule,6 testresult,7 sighting,8 owner,9 Duration,10 date,11 config,12 comment"""
TESTER = "li, dongwangx"

def write_log(message):
    '''定义log函数， 将执行过程中的步骤记录的log文档中，方便后续查看'''
    datet = datetime.now().strftime('%Y-%m-%d')
    global log_file
    log_file = "get_new_cmd_{0}.log".format(datet)
    ctime = time.strftime("%Y-%m-%d %X", time.localtime())
    with open(log_file, 'a', encoding='utf-8') as file:
        file.write("{0}   {1}\n".format(ctime, message))


def all_tcds():
    # ID,Title,Category,Test Schedule,Test owner
    tcds_list =[]
    with open(rf'schedule_testcase.csv', 'r') as alltcds:
        alltcd = list(csv.reader(alltcds))
        # print(list(alltcd))
        # print(len(list(alltcd)))
        for i in range(len(alltcd)):
            id = alltcd[i][0]
            global all_ids
            all_ids.append(id)
            title = alltcd[i][1]
            category = alltcd[i][2]
            priority = alltcd[i][3]
            weekend = alltcd[i][5]
            owner = alltcd[i][8]
            tcds_list.append((id, title, category, priority, weekend, owner))
    return tcds_list


def have_cmd():
    # ID,Title,Cmd Line
    cmd_list = []
    with open(rf'CXDIMM-CMDline 2.csv', 'r') as ctcds:
        tcdc = list(csv.reader(ctcds))
        for i in range(len(tcdc)):
            idc =  tcdc[i][0]
            global have_ids
            have_ids.append(idc)
            titlec = tcdc[i][1]
            cmdc = tcdc[i][2]
                # Hosts -- weekend --  Category -- id --  title --  command
            cmd_list.append((idc, titlec, cmdc))

    return cmd_list


def get_new_tcd(schedule=all_tcds(), cxsh_cmdline=have_cmd()):
    # tcds_list.append((id, title, category, priority, weekend, owner))
    new_tcd =[]
    for i in range(len(schedule)):
        for j in range(len(cxsh_cmdline)):
            if schedule[i][0]==cxsh_cmdline[j][0]:
                # weekend --  Owner -- Category -- id --  title --  command
                new_id = cxsh_cmdline[j][0]
                new_weekend = schedule[i][4]
                new_category = schedule[i][2]
                new_title = schedule[i][1]
                new_priority = schedule[i][3]
                new_cmd = cxsh_cmdline[j][2]
                new_owner = schedule[i][5]
                new_tcd.append((new_weekend,new_owner,new_category,new_priority,new_id,new_title,new_cmd))

    return new_tcd


def write_to_csv(cmd=get_new_tcd()):
    #'weekend', 'owner', 'category', 'priority', 'id', 'title', 'cmd'
    number =0
    with open(rf'testcae_command.csv', 'w', newline='') as newtcds:
        fileds = ['host', 'weekend', 'owner', 'category', 'priority','id', 'title', 'cmd']
        writer = csv.DictWriter(newtcds, fieldnames=fileds)
        # writer.writeheader()
        for m in range(len(get_new_tcd())):
            if get_new_tcd()[m][1].lower() == TESTER.lower():
                number += 1
                if number % 2 ==0:
                    host = host1
                else:
                    host = host2
                writer.writerow({'host': host, 'weekend': get_new_tcd()[m][0], 'owner': get_new_tcd()[m][1],
                                 'category': get_new_tcd()[m][2], 'priority': get_new_tcd()[m][3],'id': get_new_tcd()[m][4], 'title': get_new_tcd()[m][5],
                                 'cmd': get_new_tcd()[m][6]})
                write_log("add {8} tcds successfully:{0} {1} {2} {3} {4} {5} {6} {7} ".format(host,
                                                                                         get_new_tcd()[m][0],
                                                                                         get_new_tcd()[m][1],
                                                                                         get_new_tcd()[m][2],
                                                                                         get_new_tcd()[m][3],
                                                                                         get_new_tcd()[m][4],
                                                                                         get_new_tcd()[m][5],
                                                                                         get_new_tcd()[m][6],m))

            else:
                host = "null"
                writer.writerow({'host': host, 'weekend': get_new_tcd()[m][0], 'owner': get_new_tcd()[m][1],
                                 'category': get_new_tcd()[m][2], 'priority': get_new_tcd()[m][3], 'id': get_new_tcd()[m][4], 'title': get_new_tcd()[m][5],
                                 'cmd': get_new_tcd()[m][6]})
                # writer.writerow({'host':host, 'weekend':get_new_tcd()[m][1], 'category':get_new_tcd()[m][2], 'id':get_new_tcd()[m][3], 'title':get_new_tcd()[m][4], 'cmd':get_new_tcd()[m][5], 'owner':get_new_tcd()[m][6]})
                write_log("add {8} tcds successfully:{0} {1} {2} {3} {4} {5} {6} {7}".format(host,
                                                                            get_new_tcd()[m][0],get_new_tcd()[m][1],get_new_tcd()[m][2],
                                                                            get_new_tcd()[m][3],get_new_tcd()[m][4],get_new_tcd()[m][5], get_new_tcd()[m][6],m))
                # print("total {m} tcds can't find ！".format(m))
        print("\ntotal add {0} tcds successfully".format(m))


def compare_ids(all=all_ids, have=have_ids):
    # id, title, category, priority, weekend, owner
    num = 0
    # print(all, have)
    for i in range(len(all)):
        if all[i] in have:
            pass
        else:
            # write_log("This is {1} id: {0} not found command line".format(all[i],num))
            for m in range(len(all_tcds())):
                if all[i] == all_tcds()[m][0]:
                    print(all_tcds())
                    num +=1
                    # ('15010158464', 'FISHER Correctable - Memory PFD Permanent Correctables + Dual Device', 'RAS', 'WW30', 'Li, DongwangX')
                    # write_log("This is {1} id: {0} {2} {3} not found command line".format(all[i], num), all[m][4], all[m][1])
                    write_log("{0}  this is owner：{1} schedule:{2}  category: {3}  priority :{4}  id: {5} title: {6}  can't find COMMAND LINE" .format(num, all_tcds()[m][5],all_tcds()[m][4],all_tcds()[m][2],all_tcds()[m][3],all[i],all_tcds()[m][1]))
            print("total {m} tcds can't find ！".format(m))

if __name__ == '__main__':
    print("==========================START===============================")
    write_to_csv()
    print("\n===================compare ids=================================")
    compare_ids()
    print("log file in: {0}\\{1}".format(dirs, log_file))
    print("===========================Finish=============================\n")


