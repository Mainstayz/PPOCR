import os
from check_ffmpeg import check_ffmpeg_installed
import sys
import shutil


def split_frame(video_file_path, target_dir):
    dir_path = os.path.dirname(os.path.realpath(__file__))

    if not os.path.isabs(video_file_path):
        video_file_path = os.path.abspath(video_file_path)
        print("转换为绝对路径：", video_file_path)
    else:
        print("绝对路径：", video_file_path)

    print("开始拆分帧 ...")
    file_name = os.path.basename(video_file_path)
    file_name, file_ext = os.path.splitext(file_name)

    if target_dir is None:
        tmp_frames_dir = os.path.join(dir_path, "tmp_frames")
        target_dir = os.path.join(tmp_frames_dir, file_name)

    if os.path.exists(target_dir):
        shutil.rmtree(target_dir)

    os.makedirs(target_dir)

    ffmpeg_command = f"ffmpeg -i {video_file_path} -qscale:v 1 -qmin 1 -qmax 1 -vsync 0 {os.path.join(target_dir,'frame%08d.jpg')}"

    print(f"执行ffmpeg命令：{ffmpeg_command}")
    os.system(ffmpeg_command)

    print("拆分帧完成")
    return target_dir


if __name__ == "__main__":
    # 判断存在输入参数
    if len(sys.argv) < 2:
        print("请输入视频文件路径")
        exit(1)

    if not check_ffmpeg_installed():
        print("ffmpeg未安装")
        exit(1)
    # 获取当前脚步所处的目录

    # 从输入参数中获取文件名
    video_file_path = sys.argv[1]
    split_frame(video_file_path, None)
    pass
