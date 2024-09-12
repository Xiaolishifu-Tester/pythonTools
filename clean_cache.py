import shutil
import glob
import os

# 清除当前目录下所有.pyc文件
shutil.rmtree('__pycache__')

# 或者手动删除特定文件
for file in glob.glob('*.pyc'):
    os.remove(file)
