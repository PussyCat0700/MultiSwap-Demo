import os
import shutil
import subprocess
from pathlib import Path

# 设置目录路径

base_dir_str = "part_converted/"
base_dir = Path(base_dir_str)
out_dir_str = "/data0/yfliu/outputs/baseline/nonparallel/output_top200/1gbs64_visvic_sbasedonc_fromscratch/lrs3/test_samples_p100"

mp4_files = sorted(base_dir.glob("*"))
for direc in mp4_files:
    target_direc, target_id = direc.stem.split('_')[:2]
    source_mp4_dir_str = os.path.join(out_dir_str, target_direc, target_id)
    source_wav_file = source_mp4_dir_str+'_vc.mp3'
    source_mp4_file = source_mp4_dir_str+'_vc.mp4'
    print(f"🔄 Processing {source_mp4_file}")
    target_mp4_file = direc / "muteunswap.mp4"

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
        print(f"❌ Failed to process: {target_mp4_file.name}")
