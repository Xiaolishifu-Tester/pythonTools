import subprocess
def run_cmd(command):
    try:
        output = subprocess.check_output(command, shell=True, text=True)
        output = output.strip()
    except Exception as e:
        output = str(e)

    return output

a = run_cmd("pip list")
print(a)
print(a.split(" "))
