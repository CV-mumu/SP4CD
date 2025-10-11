import os
import shutil

# 配置参数
TXT_FILE = r'/home/207lab/change_detection_datasets/SYSU-CD-256/list/test.txt'          # 你的文本文件名
SOURCE_DIRS = [r'/home/207lab/change_detection_datasets/SYSU-CD-256/A', r'/home/207lab/change_detection_datasets/SYSU-CD-256/B', r'/home/207lab/change_detection_datasets/SYSU-CD-256/label']   # 原始文件夹名
TEST_DIR = r'/home/207lab/test/'                   # 要生成的目标文件夹

def main():
    # 获取当前工作目录
    base_dir = os.getcwd()
    print(f"当前工作目录: {base_dir}")

    # 检查 txt 文件是否存在
    txt_path = os.path.join(base_dir, TXT_FILE)
    if not os.path.exists(txt_path):
        print(f"错误: 找不到文件 {txt_path}")
        return

    # 创建 test 下的 A, B, label 文件夹
    for src_dir in SOURCE_DIRS:
        target_subdir = os.path.join(base_dir, TEST_DIR, src_dir)
        os.makedirs(target_subdir, exist_ok=True)

    # 读取 txt 文件中的图片名
    with open(txt_path, 'r', encoding='utf-8') as f:
        image_names = [line.strip() for line in f if line.strip()]

    # 遍历每个图片名
    for img_name in image_names:
        for src_dir in SOURCE_DIRS:
            # 源路径：./A/16000.png
            src_path = os.path.join(base_dir, src_dir, img_name)
            # 目标路径：./test/A/16000.png
            dst_path = os.path.join(base_dir, TEST_DIR, src_dir, img_name)

            # 检查是否是同一个文件（防止复制自己到自己）
            try:
                if os.path.samefile(src_path, dst_path):
                    print(f"跳过: 源和目标是同一个文件 (意外路径重叠) {src_path}")
                    continue
            except OSError:
                # 如果文件不存在，os.path.samefile 会报错，我们忽略，继续复制
                pass

            if os.path.exists(src_path):
                shutil.copy2(src_path, dst_path)
                print(f"已复制: {src_path} -> {dst_path}")
            else:
                print(f"警告: 源文件不存在 {src_path}")

    print(f"\n✅ 复制完成！目标文件夹: {os.path.join(base_dir, TEST_DIR)}")

if __name__ == "__main__":
    main()