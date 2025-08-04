import argparse
from glob import glob
import os
from pathlib import Path
import shutil
import sys

def copy_file(src, dest):
    # 获取目标目录的父目录
    dest_dir = os.path.dirname(dest)
    
    # 如果目标目录不存在，创建它
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    
    # 复制文件
    shutil.copy(src, dest)
    print(f"File copied from {src} to {dest}")

task_dict = {
    'A': '/data0/yfliu/outputs/baseline/nonparallel/output_top200/1gbs64_fvc_sbasedonc_lstmvclub_unit_finetuned/lrs3/test_samples',  # xTkKSJSqUSI/00025_test_E22icGCvGXk_00004_vc.mp3
    'V': '/data0/yfliu/outputs/baseline/nonparallel/output_top200/1gbs64_vc_eres2net_lstmvclub_unit_finetuned_1.0/lrs3/test_samples',
    'AV': '/data0/yfliu/outputs/baseline/nonparallel/output_top200/1gbs64_favc_corentinJ_lstmvclub_unit_resume30k_0.1/lrs3/av/test_samples',
}

# 构建匹配模式
base_dir = 'all_converted/lrs3'
# 构建匹配模式，匹配任何类似00003_vc.mp4的文件
pattern = os.path.join(base_dir, '*/*_vc.mp4')  # 匹配如：7kkRkhAXZGg/00003_vc.mp4, 00004_vc.mp4 等
# 获取匹配到的文件
matched_files = glob(pattern)

# 获取匹配到的文件
mp4_files = glob(pattern)
for filename in mp4_files:
    for key in task_dict.keys():
        rel_dirname = task_dict[key]
        rel_basename = Path(filename).relative_to(base_dir)
        src_path = f'{rel_dirname}/{rel_basename}'  # xTkKSJSqUSI/00025_test_E22icGCvGXk_00004
        # rel_basename = '_'.join(rel_basename.split('/')[-2:]).replace('_test_', '_to_')
        rel_basename = str(rel_basename).replace('_vc.mp4', f'_{key}.mp4')
        dest_path = f'{base_dir}/{rel_basename}'  # xTkKSJSqUSI_00016_to_E22icGCvGXk_00006
        copy_file(src_path, dest_path)