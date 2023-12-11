import os
import sys

os.environ["KMP_DUPLICATE_LIB_OK"] = "True"

import paddle
from paddleocr import PaddleOCR, draw_ocr
from PIL import Image, ImageDraw, ImageOps
import json
import shutil


# 为 pil_box  扩容
def resize_mask_box(pil_box, image_size, len):
    left, top, right, bottom = pil_box
    left = max(0, left - len)
    top = max(0, top - len)
    right = min(image_size[0], right + len)
    bottom = min(image_size[1], bottom + len)
    return left, top, right, bottom


def get_all_file_in_dir(dir, extend="jpg"):
    """
    获取某个目录下的所有文件
    :param dir: 文件夹路径
    :param extend: 文件扩展名
    :return: 文件列表
    """
    if not os.path.exists(dir):
        return []
    if not os.path.isdir(dir):
        return []
    if not dir.endswith("/"):
        dir += "/"
    # 获取文件列表
    files = os.listdir(dir)
    files = [os.path.join(dir, file) for file in files]
    files = [file for file in files if os.path.isfile(file)]
    files = [file for file in files if file.endswith(f".{extend}")]
    return files


def get_default_ocr_dir():
    file_dir = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(file_dir, "tmp_ocr_frames")


def process_orc(source_dir, target_dir, orc_lang="ch", extend="jpg"):
    orc = PaddleOCR(use_angle_cls=True, lang=orc_lang)
    process_info = None
    process_info_file = os.path.join(target_dir, f"process_info.json")
    if os.path.exists(process_info_file):
        with open(process_info_file, "r", encoding="utf-8") as f:
            process_info = json.load(f)
    else:
        process_info = {}

    all_files = get_all_file_in_dir(source_dir, extend)
    count = len(all_files)
    current_index = 0
    for file_path in all_files:
        current_index = current_index + 1
        basename = os.path.basename(file_path)
        file_name, file_ext = os.path.splitext(basename)

        print(f"process file {current_index}/{count} {basename} ...")

        if file_name in process_info:
            file_info = process_info[file_name]
        else:
            file_info = {
                "processed": False,
                "has_subtitle": False,
            }

        if file_info["processed"]:
            continue

        result = orc.ocr(file_path)
        result = result[0]
        if not result:
            file_info["processed"] = True
            process_info[file_name] = file_info
            print(f"file {basename} no subtitle")
            # 保存处理信息
            with open(process_info_file, "w", encoding="utf-8") as f:
                json.dump(process_info, f, indent=4, ensure_ascii=False)
            continue

        target_file_path = os.path.join(target_dir, file_name)

        lines = []

        image = Image.open(file_path)
        mask = Image.new("L", image.size, 0)
        draw = ImageDraw.Draw(mask)

        for line in result:
            box = line[0]
            txt = line[1][0]
            scores = line[1][1]
            lines.append(
                {
                    "box": box,
                    "txt": txt,
                    "score": scores,
                }
            )
            left = min([coord[0] for coord in box])
            top = min([coord[1] for coord in box])
            right = max([coord[0] for coord in box])
            bottom = max([coord[1] for coord in box])
            pil_box = (left, top, right, bottom)
            fix_box = resize_mask_box(pil_box, image.size, 10)
            draw.rectangle(fix_box, fill=255)  # 白色遮罩

        mask.save(f"{target_file_path}_mask{file_ext}")

        masked_image = Image.composite(
            image, Image.new("RGB", image.size, (0, 0, 0)), ImageOps.invert(mask)
        )
        masked_image.save(f"{target_file_path}_masked{file_ext}")

        file_info["lines"] = lines
        file_info["processed"] = True
        process_info[file_name] = file_info

        # 保存处理信息
        with open(process_info_file, "w", encoding="utf-8") as f:
            json.dump(process_info, f, indent=4, ensure_ascii=False)
            print(f"process file {basename} success")


if __name__ == "__main__":
    source_path = sys.argv[1]
    if not os.path.exists(source_path):
        print(f"file {source_path} not exists")
        exit(1)
    if not os.path.abspath(source_path):
        source_path = os.path.abspath(source_path)

    target_dir = get_default_ocr_dir()
    target_dir = os.path.join(target_dir, os.path.basename(source_path))
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    process_orc(source_path, target_dir)
