import os
import shutil
import subprocess
from pathlib import Path

# 设置目录路径

base_dir_str = "speakers_imgs/"
base_dir = Path(base_dir_str)
source_mp4_dir_str = "/data0/yfliu/voxceleb2/test/mp4/"
source_wav_dir_str = "/data0/yfliu/voxceleb2/audio/test/mp4"
files = [Path(x) for x in [
"speakers_imgs/id01000/CspIoS3ZZy4/00020.jpg",
"speakers_imgs/id01066/7B-KDiAofNk/00030.jpg",
"speakers_imgs/id01041/eMRxqsB3ghc/00358.jpg",
"speakers_imgs/id01298/i8N_VPTGLis/00324.jpg",
"speakers_imgs/id01437/jrXvutBWU8k/00205.jpg",
"speakers_imgs/id01106/8NsKqf8qdIE/00049.jpg",
"speakers_imgs/id01224/9gx7Y_kleU0/00064.jpg",
"speakers_imgs/id01228/FiIjEyg3qe0/00108.jpg",
"speakers_imgs/id01460/GKUwDs0BwGQ/00091.jpg",
"speakers_imgs/id01066/7B-KDiAofNk/00030.jpg",
"speakers_imgs/id01041/eMRxqsB3ghc/00358.jpg",
"speakers_imgs/id01298/i8N_VPTGLis/00324.jpg",
"speakers_imgs/id01066/FDp-ZLCWrIc/00054.jpg",
"speakers_imgs/id01106/8NsKqf8qdIE/00049.jpg",
"speakers_imgs/id01224/9gx7Y_kleU0/00064.jpg",
"speakers_imgs/id01228/FiIjEyg3qe0/00108.jpg",
  ]]

for file in files:
    target_mp4_file = file.with_suffix('.mp4')
    source_wav_file = Path(os.path.join(source_wav_dir_str, '/'.join(str(target_mp4_file).split('/')[-3:]))).with_suffix('.wav')
    source_mp4_file = Path(os.path.join(source_mp4_dir_str, '/'.join(str(target_mp4_file).split('/')[-3:]))).with_suffix('.mp4')

    print(f"🔄 Processing {target_mp4_file.name}")

    try:
        # 调用 ffmpeg 替换音轨并重新编码
        subprocess.run([
            "ffmpeg", "-y",
            "-i", str(source_mp4_file),
            "-i", str(source_wav_file),
            "-c:v", "libx264",
            "-preset", "veryfast",
            "-crf", "23",
            "-c:a", "aac",
            "-b:a", "128k",
            "-map", "0:v:0",
            "-map", "1:a:0",
            "-shortest",
            "-movflags", "+faststart",
            str(target_mp4_file)
        ], check=True)

        print(f"✅ Exported: {target_mp4_file.name}")
    except subprocess.CalledProcessError:
        print(f"❌ Failed to process: {file.name}")
