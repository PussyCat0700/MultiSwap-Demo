import os
import shutil
import subprocess
from pathlib import Path

# 设置目录路径

base_dir_str = "speakers_imgs/"
base_dir = Path(base_dir_str)
source_mp4_dir_str = "/data0/yfliu/lrs3/test"

jpg_files = sorted(base_dir.glob("*/*.jpg"))

for jpg_file in jpg_files:
    target_mp4_file = jpg_file.with_suffix(".mp4")
    source_mp3_file = Path(os.path.join(source_mp4_dir_str, '/'.join(str(jpg_file).split('/')[-2:]))).with_suffix('.flac')
    source_mp4_file = Path(os.path.join(source_mp4_dir_str, '/'.join(str(jpg_file).split('/')[-2:]))).with_suffix('.mp4')
    if not jpg_file.exists():
        print(f"⚠️  Skipping: no matching .mp4 for {jpg_file.name}")
        continue

    print(f"🔄 Processing {jpg_file.name} -> {target_mp4_file.name}")

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
        print(f"❌ Failed to process: {jpg_file.name}")
