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
    'A': '/data0/yfliu/outputs/baseline/nonparallel/output_top200/1gbs64_fvc_sbasedonc_lstmvclub_unit_finetuned/test_samples_N+swapped/mp4/',  # xTkKSJSqUSI/00025_test_E22icGCvGXk_00004_vc.mp3
    'V': '/data0/yfliu/outputs/baseline/nonparallel/output_top200/1gbs64_vc_eres2net_lstmvclub_unit_finetuned_1.0/test_samples_N+swapped/mp4/',
    'AV': '/data0/yfliu/outputs/baseline/nonparallel/output_top200/1gbs64_favc_corentinJ_lstmvclub_unit_resume30k_0.1/test_samples_N+swapped/mp4/',
}

# 构建匹配模式
base_dir = 'others_converted/'

# 获取匹配到的文件
rel_files = [
    'id01000/CspIoS3ZZy4/00020_test_mp4_id01066_7B-KDiAofNk_00030_vc.mp3',
    'id01000/CspIoS3ZZy4/00020_test_mp4_id01041_eMRxqsB3ghc_00358_vc.mp3',
    'id01000/CspIoS3ZZy4/00020_test_mp4_id01298_i8N_VPTGLis_00324_vc.mp3',
    'id01437/jrXvutBWU8k/00205_test_mp4_id01106_8NsKqf8qdIE_00049_vc.mp3',
    'id01437/jrXvutBWU8k/00205_test_mp4_id01224_9gx7Y_kleU0_00064_vc.mp3',
    'id01437/jrXvutBWU8k/00205_test_mp4_id01228_FiIjEyg3qe0_00108_vc.mp3',
    ]
for rel_basename in rel_files:
    for key in task_dict.keys():
        ckpt_basename = task_dict[key]
        src_path = f'{ckpt_basename}/{rel_basename}'  # xTkKSJSqUSI/00025_test_E22icGCvGXk_00004
        # rel_basename = '_'.join(rel_basename.split('/')[-2:]).replace('_test_', '_to_')
        dest_path = f"{base_dir}/{str(rel_basename).replace('_vc.mp3', f'_{key}.mp3')}"
        copy_file(src_path, dest_path)