"""
生成 gt_catalog.pkl 文件，包含数据集中所有独特的 (电影名, 年份) 元组。
用于 reward 计算和评估时验证推荐电影是否真实存在。
"""
import pickle
import os
from datasets import load_from_disk


def generate_catalog(dataset_path: str, output_path: str = "gt_catalog.pkl"):
    """从数据集生成电影目录"""
    catalog = set()

    # 尝试加载各个子集
    for split in ["train", "validation", "test"]:
        split_path = os.path.join(dataset_path, split)
        if os.path.exists(split_path):
            print(f"Loading {split}...")
            dataset = load_from_disk(split_path)
            for item in dataset:
                gt_list = item.get("groundtruth_with_release_year", [])
                for movie, year in gt_list:
                    catalog.add((movie, year))

    print(f"Total unique movies: {len(catalog)}")

    # 保存为 pickle
    with open(output_path, "wb") as f:
        pickle.dump(list(catalog), f)

    print(f"Catalog saved to {output_path}")
    return catalog


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset_path", type=str, 
                        default="processed_datasets/sft_dataset",
                        help="数据集路径")
    parser.add_argument("--output_path", type=str, 
                        default="gt_catalog.pkl",
                        help="输出文件路径")
    args = parser.parse_args()

    generate_catalog(args.dataset_path, args.output_path)
