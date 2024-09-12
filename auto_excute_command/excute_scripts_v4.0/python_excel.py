# coding=gb2312
import pandas as pd

file_name = r"latest_27.4_CXSH-CS2-SKU1-5600-64GB-MPS-MT-Rev-A(2Rx4).xlsx"
# data_form = pd.read_excel(open(file_name,"rb"), sheet_name= "Functional (1DPC)", dtype={"Stkcd": str})
data_form = pd.read_excel((file_name), sheet_name= "Functional (1DPC)")
# print(type(list(data_form)))
for i in range(len(list(data_form.index.values))):
# print(len(list(data_form.index.values)))
    print(list(data_form.loc[i].values))
# # print(data_file)
# # print(data_file.head())
# # print(data_file.index)
# data_file = data_form.loc[0].values  # 获取某一行的数据
# # print(data_file)
# # print(data_form.index)
# #
# # print("=======================")
# # 获取指定多行的数据
# data_file2 = data_form.loc[[0,1,2,3,4]].values
# # print(data_file2)
# # print("=========total index===========")
# # print(len(data_form.index.values)) # 获取总行
# # 获取行号输出
# index_1 = data_form.index.values
# # print(index_1)
# #
# # # 获取列名输出
# print("==============columns========")
# columns_1 = data_form.columns.values
# # print(columns_1)
# for i in range(len(data_form.index.values)):
#     print(f"===={i}==ID====",data_form.loc[i].values[1])
#
# #
# #
# for j in range(len(data_form.index.values)):
#     # print(data_form.loc[j].values)
#     pass
