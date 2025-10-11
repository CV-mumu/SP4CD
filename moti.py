import os
import cv2
import numpy as np
from skimage.measure import label, regionprops


def calc_split_ratio(binary_image, window_size=(64, 64)):
    labeled_img = label(binary_image > 0)
    regions = regionprops(labeled_img)

    total_objects = len(regions)
    if total_objects == 0:
        return 0.0, 0, 0  # 返回三个值

    obj_in_window_map = {}

    height, width = binary_image.shape
    win_h, win_w = window_size

    for y in range(0, height, win_h):
        for x in range(0, width, win_w):
            x_end = min(x + win_w, width)
            y_end = min(y + win_h, height)
            window_mask = labeled_img[y:y_end, x:x_end]

            unique_objs = set(np.unique(window_mask)) - {0}
            if not unique_objs:
                continue

            for obj_id in unique_objs:
                if obj_id not in obj_in_window_map:
                    obj_in_window_map[obj_id] = set()
                obj_in_window_map[obj_id].add((y, x))

    split_count = 0
    for obj_id, windows in obj_in_window_map.items():
        if len(windows) > 1:
            split_count += 1

    split_ratio = split_count / total_objects if total_objects > 0 else 0
    return split_ratio, split_count, total_objects  # 返回三个值


def process_folder(folder_path, window_size=(64, 64), visualize=False):
    supported_formats = ('.png', '.jpg', '.jpeg', '.bmp', '.tiff')

    total_split_count = 0
    total_object_count = 0
    ratio_list = []

    for filename in os.listdir(folder_path):
        if not filename.lower().endswith(supported_formats):
            continue

        image_path = os.path.join(folder_path, filename)
        print(f"正在处理图像: {filename}")

        # 读取图像
        binary_image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if binary_image is None:
            print(f"无法读取图像：{filename}")
            continue

        # 二值化处理（确保像素值为 0 和 1）
        _, binary_image = cv2.threshold(binary_image, 127, 1, cv2.THRESH_BINARY)

        # 计算指标
        ratio, split_count, total_objects = calc_split_ratio(binary_image, window_size)

        # 累计统计
        total_split_count += split_count
        total_object_count += total_objects
        ratio_list.append(ratio)

        print(f"  目标数: {total_objects}, 被切分数: {split_count}, 比例: {ratio:.4f}")

    # 总体统计
    avg_split_ratio = sum(ratio_list) / len(ratio_list) if ratio_list else 0

    return {
        "total_objects": total_object_count,
        "total_split_objects": total_split_count,
        "avg_split_ratio": avg_split_ratio,
    }



if __name__ == "__main__":
    folder_path = r"/home/207lab/change_detection_datasets/DSIFN-CD-256/label"  
    window_size = (256, 128)                      

    result = process_folder(folder_path, window_size=window_size)

    print("\n📊 批量处理结果汇总:")
    print(f"总目标数: {result['total_objects']}")
    print(f"总被切分的目标数: {result['total_split_objects']}")
    print(f"平均目标被切分比例: {result['avg_split_ratio']:.4f}")
