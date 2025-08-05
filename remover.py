import os
import sys

def list_files_to_delete(root_dir):
    files_to_delete = []
    
    # 遍历目录及其子目录
    for dirpath, dirnames, filenames in os.walk(root_dir, topdown=False):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            # 检查需要删除的文件
            if filename.endswith(('.png', '.jpg', '.wav')):
                files_to_delete.append(file_path)
            elif filename.endswith('.mp3') and filename != 'gt_src.mp3':
                files_to_delete.append(file_path)
            if '_vc.' in filename:
                files_to_delete.append(file_path)
    
    return files_to_delete

def confirm_and_delete(files_to_delete):
    if not files_to_delete:
        print("没有需要删除的文件。")
        return
    
    # 打印需要删除的文件
    print("以下是将要删除的文件：")
    for file in files_to_delete:
        print(file)
    
    # 用户确认
    confirm = input("\n确定要删除这些文件吗？(y/n): ")
    if confirm.lower() == 'y':
        for file in files_to_delete:
            try:
                os.remove(file)
                print(f"已删除: {file}")
            except Exception as e:
                print(f"删除文件 {file} 时出错: {e}")
    else:
        print("操作已取消。")

def main():
    # 从命令行获取目录路径
    if len(sys.argv) != 2:
        print("请提供目录路径作为参数。")
        sys.exit(1)
    
    root_dir = sys.argv[1]
    
    if not os.path.isdir(root_dir):
        print("提供的路径不是有效的目录。")
        sys.exit(1)
    
    files_to_delete = list_files_to_delete(root_dir)
    confirm_and_delete(files_to_delete)

if __name__ == '__main__':
    main()
