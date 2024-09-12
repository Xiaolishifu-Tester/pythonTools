import pandas as pd
import os

dirs = os.getcwd()
all_ids=[]; have_ids=[];total_tcds_list =[];cmdlist_tcds =[]
log_file=""
host1 ="H0701"; host2 = "H0802"; #host = "all"
# schedule_testcase_format = """0 ID, 1 Title,2 Category, 3 Priority,4 A:1DPC,5  Schedule,6 testresult,7 sighting,8 owner,9 Duration,10 date,11 config,12 comment"""
schedule_file = r"CXSH SPR DDR5-5600 Dry Run Report"
sheet_name = r"Functional (1DPC)"
command_excel = r"CXDIMM-CMDline 3.xlsx"
sheet_command = r"CXDIMM-CMDline 2"
new_command_excel = rf"{schedule_file}_schedule.xlsx"
not_find_excel = rf"Not_find_cmd_{schedule_file}.xlsx"
TESTER = "Li, DongwangX"
dicts = []

df = pd.read_excel(f"{schedule_file}.xlsx", sheet_name=sheet_name)
# print(df.columns)
headers = df.columns
for i in range(len(headers)):
    dict ={i, headers[i]}
    dicts.append(dict)

print(dicts)