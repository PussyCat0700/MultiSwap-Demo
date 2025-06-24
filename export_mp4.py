import os
import shutil
import subprocess
from pathlib import Path

# 设置目录路径

base_dir_str = "all_converted/lrs3"
base_dir = Path(base_dir_str)
os.makedirs(base_dir_str, exist_ok=True)
source_lip_dir_str = "/data0/yfliu/lrs3/video/test/"  # simply copy
source_lip_dir = Path(source_lip_dir_str)
source_ful_dir_str = "/data0/yfliu/lrs3/test/"  # has flac
source_ful_dir = Path(source_ful_dir_str)
out_dir_str = "/data0/yfliu/outputs/baseline/nonparallel/output_top200/1gbs64_visvic_sbasedonc_fromscratch/lrs3/"
out_dir = Path(out_dir_str)

mp4_files = {'source': {}, 'target':{}, 'unswapped': {}, 'swapped': {}}
for source in ["E22icGCvGXk/00001", "sxnlvwprfSc/00003", "9uOMectkCCs/00002", "7kkRkhAXZGg/00006"]:
    source_spk = str(source).split('/')[0]
    mp4_file = out_dir / "test_samples_p100" / f'{str(source)}_vc.mp4'
    mp4_files['unswapped'].setdefault(source_spk, []).append(mp4_file)
    mp4_file = source_lip_dir / f'{source}.mp4'
    mp4_files["source"].setdefault(source_spk, []).append(mp4_file)
    for target in ["UAj1hsXp18c_00003", "UAj1hsXp18c_00012",
                    "ZJNESMhIxQ0_00003", "ZJNESMhIxQ0_00021",
                    "mgcjr1yz7ow_00002", "mgcjr1yz7ow_00003",
                    "xTkKSJSqUSI_00004", "xTkKSJSqUSI_00012",]:
        mp4_file = out_dir / "test_samples_N+swapped" / f'{str(source)}_test_{str(target)}_vc.mp4'
        mp4_files['swapped'].setdefault(source_spk, []).append(mp4_file)
        target_spk, target_id = target.split('_')
        mp4_file = source_ful_dir / target_spk / f'{target_id}.mp4'
        mp4_files['target'].setdefault(target_spk, []).append(mp4_file)
for category_key, mp4_dicts in mp4_files.items():
    for spk, mp4_files in mp4_dicts.items():
        os.makedirs(base_dir / spk, exist_ok=True)
        for mp4_file in mp4_files:
            print(f"🔄 Processing {mp4_file}")
            target_mp4_file = base_dir / spk / f'{mp4_file.stem}.mp4'
            if category_key in ['swapped', 'unswapped']:
                source_wav_file = mp4_file.with_suffix('.mp3')
                source_mp4_file = mp4_file.with_suffix('.mp4')
            elif category_key == 'target':
                source_wav_file = mp4_file.with_suffix('.flac')
                source_mp4_file = mp4_file.with_suffix('.mp4')
            elif category_key == 'source':
                # simply copy
                shutil.copy(mp4_file, target_mp4_file)
                print(f"✅ Exported: {target_mp4_file.name}")
                continue

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
