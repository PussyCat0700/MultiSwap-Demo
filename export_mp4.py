from glob import glob
import os
import shutil
import subprocess
from pathlib import Path

# 设置目录路径

# base_dir_str = "speakers_imgs/"
# base_dir = Path(base_dir_str)
# source_wav_dir_str = "/data0/yfliu/outputs/baseline/nonparallel/output_top200/1gbs64_visvic_sbasedonc_fromscratch/vox2/test_samples/mp4/"
# source_mp4_dir_str = source_wav_dir_str
# target_mp4_dir_str = "others_converted/"

# files = [
# "id01000/CspIoS3ZZy4/00020_vc.mp4",
# "id01066/7B-KDiAofNk/00030_vc.mp4",
# "id01298/i8N_VPTGLis/00324_vc.mp4",
# "id01041/eMRxqsB3ghc/00358_vc.mp4",
# "id01437/jrXvutBWU8k/00205_vc.mp4",
# "id01106/8NsKqf8qdIE/00049_vc.mp4",
# "id01224/9gx7Y_kleU0/00064_vc.mp4",
# "id01228/FiIjEyg3qe0/00108_vc.mp4",
# "id01460/GKUwDs0BwGQ/00091_vc.mp4",
# "id01066/7B-KDiAofNk/00030_vc.mp4",
# "id01041/eMRxqsB3ghc/00358_vc.mp4",
# "id01298/i8N_VPTGLis/00324_vc.mp4",
# "id01066/7B-KDiAofNk/00030_vc.mp4",
# "id01106/8NsKqf8qdIE/00049_vc.mp4",
# "id01224/9gx7Y_kleU0/00064_vc.mp4",
# "id01228/FiIjEyg3qe0/00108_vc.mp4",
# ]

# for mp4_file in files:
#     source_mp3_file = (Path(source_wav_dir_str) / mp4_file).with_suffix('.mp3')
#     source_mp4_file = (Path(source_mp4_dir_str) / mp4_file).with_suffix('.mp4')
#     target_mp4_file = Path(target_mp4_dir_str) / mp4_file
#     target_tmp_file = target_mp4_file.with_name(target_mp4_file.stem + "_temp.mp4")
#     os.makedirs(target_mp4_file.parent, exist_ok=True)
#     print(f"🔄 Processing {target_mp4_file.name}")

#     try:
#         # 调用 ffmpeg 替换音轨并重新编码
#         subprocess.run([
#             "ffmpeg", "-y",
#             "-i", str(source_mp4_file),
#             "-i", str(source_mp3_file),
#             "-c:v", "libx264",
#             "-preset", "veryfast",
#             "-crf", "23",
#             "-c:a", "aac",
#             "-b:a", "128k",
#             "-map", "0:v:0",
#             "-map", "1:a:0",
#             "-shortest",
#             "-movflags", "+faststart",
#             str(target_tmp_file)
#         ], check=True)
        
#         target_tmp_file.replace(target_mp4_file)

#         print(f"✅ Exported: {target_mp4_file.name}")
#     except subprocess.CalledProcessError:
#         print(f"❌ Failed to process: {target_mp4_file.name}")

# 构建匹配模式
base_dir = audio_base_dir = './others_converted'
matched_files = [
    'id01000/CspIoS3ZZy4/00020_test_mp4_id01066_7B-KDiAofNk_00030_vc.mp3',
    'id01000/CspIoS3ZZy4/00020_test_mp4_id01041_eMRxqsB3ghc_00358_vc.mp3',
    'id01000/CspIoS3ZZy4/00020_test_mp4_id01298_i8N_VPTGLis_00324_vc.mp3',
    'id01437/jrXvutBWU8k/00205_test_mp4_id01106_8NsKqf8qdIE_00049_vc.mp3',
    'id01437/jrXvutBWU8k/00205_test_mp4_id01224_9gx7Y_kleU0_00064_vc.mp3',
    'id01437/jrXvutBWU8k/00205_test_mp4_id01228_FiIjEyg3qe0_00108_vc.mp3',
    ]
postfixes = ['A', 'V', 'AV']
for filename in matched_files:
    for postfix in postfixes:
        rel_dir_source = Path(filename.replace('_vc.mp3', f'_{postfix}.mp3'))
        source_mp3_file = Path(f'{base_dir}/{rel_dir_source}')
        target_mp4_file = source_mp3_file.with_suffix('.mp4')
        rel_dir_target = Path(filename.replace('_vc.mp3', f'_vc.mp4'))
        source_mp4_file = Path(f'{audio_base_dir}/{rel_dir_target}')
        target_tmp_file = target_mp4_file.with_name(target_mp4_file.stem + "_temp.mp4")
        subprocess.run([
        "ffmpeg", "-y",
        "-i", str(source_mp4_file),
        "-i", str(source_mp3_file),
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "23",
        "-c:a", "aac",
        "-b:a", "128k",
        "-map", "0:v:0",
        "-map", "1:a:0",
        "-shortest",
        "-movflags", "+faststart",
        str(target_tmp_file)
        ], check=True)
        
        target_tmp_file.replace(target_mp4_file)

        print(f"✅ Exported: {target_mp4_file.name}")