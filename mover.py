import argparse
import os
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

# # 设置命令行参数
# parser = argparse.ArgumentParser(description='Copy a file to a specified directory.')
# parser.add_argument('wavpath')
# # 解析参数
# args = parser.parse_args()

# 示例路径
# src_path = f'/data0/yfliu/voxceleb2/frames/test/mp4/{args.wavpath}'
# dest_path = f'speakers_imgs/{args.wavpath}'
# src_path = f'/data0/yfliu/voxceleb2/audio/test/mp4/{args.wavpath}.wav'
# dest_path = f'others_converted/{args.wavpath}.wav'
# copy_file(src_path, dest_path)

task_dict = {
    # 'SP-FaceVC': '/data0/yfliu/lrs3/spfacevc/syn_clean',  # xTkKSJSqUSI_00025_E22icGCvGXk_00004_synthesis.wav
    # 'FVMVC': '/data0/yfliu/outputs/zero_shot_facevc/lrs3/wav/test_samples_N+swapped',  # xTkKSJSqUSI_00025_test_E22icGCvGXk_00004_gen.wav
    'MultiSwap-A': '/data0/yfliu/outputs/baseline/nonparallel/output_top200/1gbs64_fvc_sbasedonc_lstmvclub_unit_finetuned/lrs3/test_samples_N+swapped',  # xTkKSJSqUSI/00025_test_E22icGCvGXk_00004_vc.mp3
    'MultiSwap-V': '/data0/yfliu/outputs/baseline/nonparallel/output_top200/1gbs64_vc_eres2net_lstmvclub_unit_finetuned_1.0/lrs3/test_samples_N+swapped',
    'MultiSwap-AV': '/data0/yfliu/outputs/baseline/nonparallel/output_top200/1gbs64_favc_corentinJ_lstmvclub_unit_resume30k_0.1/lrs3/av/test_samples_N+swapped',
    # 'MuteSwap': '/data0/yfliu/outputs/baseline/nonparallel/output_top200/1gbs64_visvic_sbasedonc_fromscratch/lrs3/test_samples_N+swapped',
    'MultiSwap-O (A)': '/data0/yfliu/outputs/baseline/nonparallel/output_top200/4gbs64_favc_corentinJ_lstmvclub_unit_resumed15k_0.1_5050/lrs3/a/test_samples_N+swapped',
    'MultiSwap-O (V)': '/data0/yfliu/outputs/baseline/nonparallel/output_top200/4gbs64_favc_corentinJ_lstmvclub_unit_resumed15k_0.1_5050/lrs3/v/test_samples_N+swapped',
    'MultiSwap-O (AV)': '/data0/yfliu/outputs/baseline/nonparallel/output_top200/4gbs64_favc_corentinJ_lstmvclub_unit_resumed15k_0.1_5050/lrs3/av/test_samples_N+swapped',
}


wavpaths= ['mgcjr1yz7ow/00016_test_7kkRkhAXZGg_00006', 'UAj1hsXp18c/00012_test_sxnlvwprfSc_00001', 'xTkKSJSqUSI/00016_test_E22icGCvGXk_00006', 'ZJNESMhIxQ0/00004_test_9uOMectkCCs_00002']
for wavpath in wavpaths:
    for key in task_dict.keys():
        rel_dirname = task_dict[key]
        rel_basename = wavpath
        src_path = f'{rel_dirname}/{rel_basename}_vc.mp3'  # xTkKSJSqUSI/00025_test_E22icGCvGXk_00004
        rel_basename = '_'.join(rel_basename.split('/')[-2:]).replace('_test_', '_to_')
        dest_path = f'part_converted/{rel_basename}/{key}.mp3'  # xTkKSJSqUSI_00016_to_E22icGCvGXk_00006
        copy_file(src_path, dest_path)