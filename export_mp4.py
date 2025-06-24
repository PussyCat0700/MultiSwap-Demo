import os
import shutil
import subprocess
from pathlib import Path

# 设置目录路径

base_dir_str = "speakers_imgs/"
base_dir = Path(base_dir_str)
source_mp4_dir_str = "/data0/yfliu/lrs3/audio/test"
target_mp4_dir_str = "all_converted/lrs3"

files = [
  "7kkRkhAXZGg/00006.mp4",
  "9uOMectkCCs/00002.mp4",
  "E22icGCvGXk/00001.mp4",
  "sxnlvwprfSc/00003.mp4",
]

for mp4_file in files:
    source_mp3_file = (Path(source_mp4_dir_str) / mp4_file).with_suffix('.wav')
    source_mp4_file = target_mp4_file = Path(target_mp4_dir_str) / mp4_file
    target_tmp_file = target_mp4_file.with_name(target_mp4_file.stem + "_temp.mp4")

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
            str(target_tmp_file)
        ], check=True)
        
        target_tmp_file.replace(target_mp4_file)

        print(f"✅ Exported: {target_mp4_file.name}")
    except subprocess.CalledProcessError:
        print(f"❌ Failed to process: {target_mp4_file.name}")
