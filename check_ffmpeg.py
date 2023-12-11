# 检测 ffmpeg 是否已经安装

import subprocess
import platform


def check_ffmpeg_installed():
    # 获取当前操作系统类型
    system = platform.system()

    # 命令根据不同的操作系统进行调整
    if system == "Windows":
        command = "where ffmpeg"
    elif system == "Darwin":
        command = "which ffmpeg"
    else:
        # 如果不是 Windows 或 Mac 系统，则不支持
        print("Sorry, this function only supports Windows and Mac systems.")
        return False

    # 运行命令并获取输出
    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        print("ffmpeg is installed on your system.")
        return True
    except subprocess.CalledProcessError:
        print("ffmpeg is not installed on your system.")
        return False
