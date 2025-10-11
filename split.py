import os
import shutil

# 配置参数
TXT_FILE = r'/home/207lab/change_detection_datasets/SYSU-CD-256/list/test.txt'          
SOURCE_DIRS = [r'/home/207lab/change_detection_datasets/SYSU-CD-256/A', r'/home/207lab/change_detection_datasets/SYSU-CD-256/B', r'/home/207lab/change_detection_datasets/SYSU-CD-256/label']   # 原始文件夹名
TEST_DIR = r'/home/207lab/test/'                  

def main():
    
    base_dir = os.getcwd()
    print(f"当前工作目录: {base_dir}")

    
    txt_path = os.path.join(base_dir, TXT_FILE)
    if not os.path.exists(txt_path):
        print(f"错误: 找不到文件 {txt_path}")
        return

    
    for src_dir in SOURCE_DIRS:
        target_subdir = os.path.join(base_dir, TEST_DIR, src_dir)
        os.makedirs(target_subdir, exist_ok=True)

    
    with open(txt_path, 'r', encoding='utf-8') as f:
        image_names = [line.strip() for line in f if line.strip()]

    
    for img_name in image_names:
        for src_dir in SOURCE_DIRS:
            # 源路径：./A/16000.png
            src_path = os.path.join(base_dir, src_dir, img_name)
            # 目标路径：./test/A/16000.png
            dst_path = os.path.join(base_dir, TEST_DIR, src_dir, img_name)

            
            try:
                if os.path.samefile(src_path, dst_path):
                    print(f"跳过: 源和目标是同一个文件 (意外路径重叠) {src_path}")
                    continue
            except OSError:
              
                pass

            if os.path.exists(src_path):
                shutil.copy2(src_path, dst_path)
                print(f"已复制: {src_path} -> {dst_path}")
            else:
                print(f"警告: 源文件不存在 {src_path}")

    print(f"\n 复制完成！目标文件夹: {os.path.join(base_dir, TEST_DIR)}")

if __name__ == "__main__":
    main()
