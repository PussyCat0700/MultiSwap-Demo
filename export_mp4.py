import shutil
import subprocess
from pathlib import Path

# 设置目录路径
full_callsign = 'xTkKSJSqUSI_00016_to_E22icGCvGXk_00006'.split('_')
source_spk = full_callsign[0]
source_id = full_callsign[1]
trgt_dest = '_'.join(full_callsign[3:])

base_dir_str = f"part_converted/{source_spk}_{source_id}_to_{trgt_dest}/"
base_dir = Path(base_dir_str)
shutil.copy(f"/data0/yfliu/outputs/baseline/nonparallel/output_top200/1gbs64_visvic_sbasedonc_fromscratch/lrs3/test_samples_N+swapped/{source_spk}/{source_id}_test_{trgt_dest}_vc.mp3", base_dir_str+"muteswap.mp3")
shutil.copy(f"/data0/yfliu/lrs3/video/test/{source_spk}/{source_id}.mp4", base_dir_str+"lipregion.mp4")

# 查找所有 .mp3 文件
mp3_files = sorted(base_dir.glob("*.mp3"))

for mp3_file in mp3_files:
    target_mp4_file = mp3_file.with_suffix(".mp4")
    if not target_mp4_file.exists():
        source_mp4_file = base_dir / 'gt_src.mp4'
    else:
        source_mp4_file = target_mp4_file
    temp_file = mp3_file.with_name(mp3_file.stem + "_temp.mp4")

    if not source_mp4_file.exists():
        print(f"⚠️  Skipping: no matching .mp4 for {mp3_file.name}")
        continue

    print(f"🔄 Processing {mp3_file.name} -> {target_mp4_file.name}")

    try:
        # 调用 ffmpeg 替换音轨并重新编码
        subprocess.run([
            "ffmpeg", "-y",
            "-i", str(source_mp4_file),
            "-i", str(mp3_file),
            "-c:v", "libx264",
            "-preset", "veryfast",
            "-crf", "23",
            "-c:a", "aac",
            "-b:a", "128k",
            "-map", "0:v:0",
            "-map", "1:a:0",
            "-shortest",
            "-movflags", "+faststart",
            str(temp_file)
        ], check=True)

        # 覆盖原始 mp4
        temp_file.replace(target_mp4_file)
        print(f"✅ Exported: {target_mp4_file.name}")
    except subprocess.CalledProcessError:
        print(f"❌ Failed to process: {mp3_file.name}")


table_content = f"""
<table align="center" style="text-align: center; border-collapse: collapse;">
            <thead>
              <tr>
                <td></td>
                <td colspan="2"><b>FVC</b></td>
                <td colspan="1"><b>SFVC</b></td>
                <td colspan="1"><b>Reference Video</td>
              </tr>
              <tr>
                <td></td>
                <td>Source Video</td>
                <td>Source Video (Noised)</td>
                <td>Silent Lip</td>
                <td>Image Source</td>
              </tr>
            </thead>
          
            <tbody>
              <tr>
                <td><b>Inputs</b></td>
                <td><video controls style="width:200px;height:200px;"><source src="part_converted/{source_spk}_{source_id}_to_{trgt_dest}/gt_src.mp4" type="video/mp4"></video></td>
                <td><video controls style="width:200px;height:200px;"><source src="part_converted/{source_spk}_{source_id}_to_{trgt_dest}/gt_src_noised.mp4" type="video/mp4"></video></td>
                <td><video controls style="width:200px;height:200px;"><source src="part_converted/{source_spk}_{source_id}_to_{trgt_dest}/lipregion.mp4" type="video/mp4"></video></td>
                <td><video controls style="width:200px;height:200px;"><source src="part_converted/{source_spk}_{source_id}_to_{trgt_dest}/gt_tgt.mp4" type="video/mp4"></video></td>
              </tr>
          
              <tr>
                <td><b>FVMVC</b></td>
                <td><video controls style="width:150px;height:150px;"><source src="part_converted/{source_spk}_{source_id}_to_{trgt_dest}/fvmvc.mp4" type="video/mp4"></video></td>
                <td><video controls style="width:150px;height:150px;"><source src="part_converted/{source_spk}_{source_id}_to_{trgt_dest}/fvmvc_noised.mp4" type="video/mp4"></video></td>
                <td rowspan="2"><video controls style="width:150px;height:150px;"><source src="part_converted/{source_spk}_{source_id}_to_{trgt_dest}/muteswap.mp4" type="video/mp4"></video><br><b>MuteSwap</b></td>
                <td></td>
              </tr>
          
              <tr>
                <td><b>SP-FaceVC</b></td>
                <td><video controls style="width:150px;height:150px;"><source src="part_converted/{source_spk}_{source_id}_to_{trgt_dest}/sp_facevc.mp4" type="video/mp4"></video></td>
                <td><video controls style="width:150px;height:150px;"><source src="part_converted/{source_spk}_{source_id}_to_{trgt_dest}/sp_facevc_noised.mp4" type="video/mp4"></video></td>
                <td></td>
              </tr>
            </tbody>
          </table>
"""
print(table_content)