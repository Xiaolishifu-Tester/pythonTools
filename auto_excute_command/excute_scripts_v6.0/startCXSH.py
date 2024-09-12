# coding = utf-8
import csv, os, sys, time
from datetime import datetime
import pandas as pd

GETARGV1 = sys.argv[1]
TESTCASEFORMEXCEL = rf"testcase_running_command.xlsx"
sheet_name = rf"Sheet1"
ALLTCDSFROMTESTFILE = []
GETCWD = os.getcwd()
SCRIPTSDIR = rf"C:\PY\IPU\CXSH"   # C:\CXSH\bifrost\bifrost\release  C:\PY\IPU\CXSH\
CURRENTCTIMES = time.strftime("%Y-%m-%d %X", time.localtime())
CTIMES = CURRENTCTIMES.split(" ")
CTIMES1 = CTIMES[1].split(":")
CTIME = rf"{CTIMES1[0]}_{CTIMES1[1]}_{CTIMES1[2]}"
TIMES = rf"{CTIMES[0]}_{CTIME}"
ALLHOSTS = {"H0701": "801020", "H0802": "801023", "all":"118"}  # dict   add ,Keys:Values
test_result_excel = rf"test_result_{TIMES}.xlsx"
date_folder = datetime.now().date()
folder_path = fr"{GETCWD}\{date_folder}"
if not os.path.exists(fr"{folder_path}"):
    os.makedirs(folder_path)




def getAllTCDs(testfile=TESTCASEFORMEXCEL):
    # fileds = ['host', 'weekend', 'owner', 'category', 'priority', 'id', 'title', 'cmd']
    os.chdir(GETCWD)
    data_form = pd.read_excel((TESTCASEFORMEXCEL), sheet_name=sheet_name)
    global ALLTCDSFROMTESTFILE
    for num in range(len(list(data_form.index.values))):
        ALLTCDSFROMTESTFILE.append(list(data_form.loc[num].values))


def excutionAllTcd(ids):
    getAllTCDs()
    # fileds = ['host', 'weekend', 'owner', 'category', 'priority', 'id', 'title', 'cmd']
    os.chdir(folder_path)
    excel_head = pd.DataFrame(
        {'date': [], 'result': [],'id': [], 'title': [], 'duration': [], 'test_config': [], 'host':[],'weekend': [], 'owner': [],
         'category': [],
         'priority': [],
         'cmd': []})
    excel_head.to_excel(test_result_excel, header=True, index=False)
    for j in range(len(ALLTCDSFROMTESTFILE)):
        # print(type(ALLTCDSFROMTESTFILE[j][5]))
        host = ALLTCDSFROMTESTFILE[j][0]
        weekend = ALLTCDSFROMTESTFILE[j][1]
        owner = ALLTCDSFROMTESTFILE[j][2]
        category = ALLTCDSFROMTESTFILE[j][3]
        priority = ALLTCDSFROMTESTFILE[j][4]
        id = ALLTCDSFROMTESTFILE[j][5]
        title = ALLTCDSFROMTESTFILE[j][6]
        cmd = ALLTCDSFROMTESTFILE[j][7]
        currenttimes = time.strftime("%Y-%m-%d %X", time.localtime())
        if str(ALLTCDSFROMTESTFILE[j][5]) == ids:
            os.chdir(SCRIPTSDIR)
            stime = time.time()
            exit_code = os.system(rf'{ALLTCDSFROMTESTFILE[j][7]}')
            if exit_code == 0:
                test_result = "PASS"
            else:
                test_result = "FAIL"
            etime = time.time()
            host_key = ALLHOSTS.get(host)
            os.chdir(folder_path)
            df = pd.DataFrame({'date': [currenttimes], 'result': [test_result], 'id': [id], 'title': [title],
                               'duration': [etime - stime], 'test_config': [host_key], 'host': [host],
                               'weekend': [weekend], 'owner': [owner],
                               'category': [category], 'priority': [priority], 'cmd': [cmd]})
            with pd.ExcelWriter(test_result_excel, engine="openpyxl", mode="a", if_sheet_exists="overlay") as writer:
                df.to_excel(writer, sheet_name="Sheet1", startrow=writer.sheets['Sheet1'].max_row, header=False,
                            index=False)


if __name__ == '__main__':
    get_argv = input("Please input your excute type:(testenv or id1, ids2):")
    if get_argv.upper() == "TESTENV":
        excutionAllTcd("118119120")
    else:
        ids = get_argv.split(",")
        for num in range(len(ids)):
            excutionAllTcd(ids[num])





