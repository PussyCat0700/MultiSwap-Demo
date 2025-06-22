import os
import shutil
import subprocess
from pathlib import Path

# 设置目录路径

base_dir_str = "speakers_imgs/"
base_dir = Path(base_dir_str)
source_mp4_dir_str = "/data0/yfliu/lrs3/test"

files = [Path(x) for x in [
  "speakers_imgs/UAj1hsXp18c/00011.mp4",
  "speakers_imgs/81Ub0SMxZQo/00001.mp4",
  "speakers_imgs/xTkKSJSqUSI/00008.mp4",
  "speakers_imgs/E22icGCvGXk/00006.mp4",
  "speakers_imgs/ZJNESMhIxQ0/00020.mp4",
  "speakers_imgs/FFG2rilqT2g/00003.mp4",
  ]]

for target_mp4_file in files:
    source_mp3_file = Path(os.path.join(source_mp4_dir_str, '/'.join(str(target_mp4_file).split('/')[-2:]))).with_suffix('.flac')
    source_mp4_file = Path(os.path.join(source_mp4_dir_str, '/'.join(str(target_mp4_file).split('/')[-2:]))).with_suffix('.mp4')

    print(f"🔄 Processing {target_mp4_file.name}")

    try:
        # 调用 ffmpeg 替换音轨并重新编码
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
            str(target_mp4_file)
        ], check=True)

        print(f"✅ Exported: {target_mp4_file.name}")
    except subprocess.CalledProcessError:
        print(f"❌ Failed to process: {file.name}")
