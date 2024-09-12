# 连接windows
import winrm

# ip地址：端口号
# winrm server端口号
# auth：用户名和密码
import os


# 连接windows
import winrm
import codecs

def exec_cmd(self, cmd):
    """
    执行cmd命令，获取返回值
    :param cmd:
    :return:
    """
    # CMD
    result = self.run_cmd(cmd)
    # powerShell
    # result = self.session.run_ps(cmd)
    # 返回码
    # code为0代表调用成功
    code = result.status_code

    # 根据返回码，获取响应内容（bytes）
    content = result.std_out if code == 0 else result.std_err

    # 转为字符串（尝试通过UTF8、GBK进行解码）
    # result = content.decode("utf8")
    # result = codecs.decode(content,'UTF-8')
    try:
        result = content.decode("utf8")
    except:
        result = content.decode("GBK")
    return code


if __name__ == "__main__":
# # 打开文件D:/py/log/trade.log
# # windows使用type命令，查看文件内容
    Connect_session = winrm.Session("10.239.12.235:5985", auth=('general', 'Passw0rd'), transport='ntlm')
    commands = r"C: &cd C:\Users\General\Desktop\IPU\autoCMD &python auto_run_cxsh_latest_gnripu_0302.py --p --H0302 --CR-ME"
    result = exec_cmd(Connect_session,commands)

    # 查看结果
    print()
