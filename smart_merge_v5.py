#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
智能注释修复脚本

本脚本是通过 git diff 工具进行注释修复的。

具体流程：
1. 使用 restore.sh 脚本拷贝最新的英文版本到本项目
2. 通过本脚本获取 git diff 获取最新提交和修改内容之间的差异，还原不需要修改的注释内容

工作原理：
- 通过 git diff --no-prefix -U99999 获取完整的文件差异信息
- 跳过 diff 元信息（diff --git, index, ---, +++, @@ 等行）
- 对于 /** */ 注释块：
  * 如果注释块既有中文又有英文 → 移除英文部分，保留中文注释
  * 如果注释块只有英文或只有中文 → 按正常 diff 规则处理
- 对于非注释内容：
  * '-' 开头的行 → 删除（不包含在最终结果中）
  * '+' 开头的行 → 添加（包含在最终结果中）
  * ' ' 开头的行 → 保持不变（包含在最终结果中）

使用方法：
python smart_merge_v5.py <源码目录>

示例：
python smart_merge_v5.py test/src

注意事项：
- 确保在 git 仓库中运行此脚本
- 建议在运行前备份重要文件
- 脚本会递归处理所有 .ts 和 .tsx 文件
"""

import os
import re
import subprocess
import sys
from pathlib import Path
from typing import List


class DiffBasedMerger:
    comment_start = "/**"
    comment_start2 = "/*"
    comment_end = "*/"

    def __init__(self, target_dir: str):
        self.target_dir = Path(target_dir)

    def get_full_diff(self, file_path: str) -> str:
        """获取完整的diff内容"""
        try:
            cmd = ["git", "diff", "--no-prefix", "-U99999", file_path]
            result = subprocess.run(
                cmd, capture_output=True, text=True, cwd=self.target_dir
            )
            return result.stdout
        except Exception as e:
            print(f"获取diff失败 {file_path}: {e}")
            return ""

    def skip_diff_header(self, diff_lines: List[str]) -> int:
        """跳过diff元信息，返回内容开始的行号"""
        for i, line in enumerate(diff_lines):
            if (
                line.startswith("diff --git")
                or line.startswith("index ")
                or line.startswith("--- ")
                or line.startswith("+++ ")
                or line.startswith("@@")
            ):
                continue
            else:
                return i
        return len(diff_lines)

    def has_chinese(self, text: str) -> bool:
        """检查是否包含中文"""
        return bool(re.search(r"[\u4e00-\u9fff]", text))

    def has_english(self, text: str) -> bool:
        """检查是否包含英文单词"""
        return bool(re.search(r"[a-zA-Z]{2,}", text))

    def remove_english_from_comment_block(self, comment_lines: List[str]) -> List[str]:
        """从注释块中移除英文，保留中文"""
        result = []

        for line in comment_lines:
            prefix = line[0] if line else " "
            content = line[1:] if len(line) > 1 else ""

            if prefix == "-":
                # 删除的行（原中文），保留
                result.append(content)
            elif prefix == "+":
                # 添加的行（新英文），需要删除
                continue
            elif prefix == " ":
                # 未修改的行，保留
                result.append(content)

        return result

    def extract_comment_block(
        self, content_lines: List[str], start_index: int
    ) -> tuple[List[str], int]:
        """提取完整的注释块，返回(注释块行列表, 下一个处理的索引)"""
        comment_lines = []
        i = start_index

        while i < len(content_lines):
            line = content_lines[i]
            if not line:
                i += 1
                continue

            comment_lines.append(line)
            content = line[1:] if len(line) > 1 else ""

            # 如果遇到注释结束标记，结束提取
            if self.comment_end in content:
                i += 1
                break
            i += 1

        return comment_lines, i

    def process_comment_block(self, comment_lines: List[str]) -> List[str]:
        """处理注释块"""
        # 提取注释块的纯文本内容（去掉diff前缀）
        comment_content = ""
        for line in comment_lines:
            prefix = line[0] if line else " "
            content = line[1:] if len(line) > 1 else ""
            comment_content += line + "\n"

        # 检查注释块是否既有中文又有英文
        if self.has_chinese(comment_content) and self.has_english(comment_content):
            # 移除英文，保留中文
            return self.remove_english_from_comment_block(comment_lines)
        else:
            # 按正常diff规则处理
            result = []
            for line in comment_lines:
                prefix = line[0] if line else " "
                content = line[1:] if len(line) > 1 else ""

                if prefix == "-":
                    # 删除的行，不包含在结果中
                    continue
                elif prefix == "+" or prefix == " ":
                    # 添加的行或未修改的行
                    result.append(content)
            return result

    def process_diff_content(self, diff_lines: List[str]) -> List[str]:
        """处理diff内容，生成最终文件"""
        start_index = self.skip_diff_header(diff_lines)
        content_lines = diff_lines[start_index:]

        result_lines = []
        i = 0

        while i < len(content_lines):
            line = content_lines[i]
            if not line:
                i += 1
                continue

            prefix = line[0] if line else " "
            content = line[1:] if len(line) > 1 else ""

            # 检查是否是注释块的开始
            if self.comment_start in content or self.comment_start2 in content:
                # 处理整个注释块
                comment_block, next_index = self.extract_comment_block(content_lines, i)

                # 需要判断下一行是否存在，如果存在判断是否开头是减号，如果是减号则注释快整体删除
                if next_index < len(content_lines):
                    next_line = content_lines[next_index]
                    if next_line.startswith("-"):
                        # 删除整个注释块
                        i = next_index
                        continue

                processed_block = self.process_comment_block(comment_block)
                result_lines.extend(processed_block)
                i = next_index
            else:
                # 非注释内容，按正常diff规则处理
                if prefix == "-":
                    # 删除的行，不包含在结果中
                    pass
                elif prefix == "+":
                    # 添加的行
                    result_lines.append(content)
                elif prefix == " ":
                    # 未修改的行
                    result_lines.append(content)
                i += 1

        return result_lines

    def process_file(self, file_path: str) -> bool:
        """处理单个文件"""
        rel_path = os.path.relpath(file_path, self.target_dir)

        # 获取diff内容
        diff_content = self.get_full_diff(rel_path)
        if not diff_content:
            return False  # 没有diff或获取失败

        # 处理diff
        diff_lines = diff_content.split("\n")
        result_lines = self.process_diff_content(diff_lines)

        # 写入文件
        try:
            full_path = self.target_dir / rel_path
            with open(full_path, "w", encoding="utf-8") as f:
                f.write("\n".join(result_lines) + "\n")
            return True
        except Exception as e:
            print(f"写入文件失败 {rel_path}: {e}")
            return False

    def get_typescript_files(self) -> List[str]:
        """递归获取所有TypeScript文件"""
        ts_files = []
        for root, dirs, files in os.walk(self.target_dir):
            for file in files:
                if file.endswith(".ts") or file.endswith(".tsx"):
                    ts_files.append(os.path.join(root, file))
        return ts_files

    def process_all_files(self):
        """处理所有TypeScript文件"""
        print("开始基于diff合并文件...")

        ts_files = self.get_typescript_files()
        total_count = len(ts_files)
        modified_count = 0

        for file_path in ts_files:
            rel_path = os.path.relpath(file_path, self.target_dir)

            if self.process_file(file_path):
                modified_count += 1
                print(f"处理文件: ✓ 已处理 ============ {rel_path}  ")
            else:
                print(f"处理文件: - 无变更 ============ {rel_path}  ")

        print(f"\n=== 处理完成 ===")
        print(f"总文件数: {total_count}")
        print(f"处理文件数: {modified_count}")
        print(f"无变更文件数: {total_count - modified_count}")


def main():
    if len(sys.argv) != 2:
        print("用法: python smart_merge_v5.py <源码目录>")
        print("示例: python smart_merge_v5.py /path/to/typescript/project")
        sys.exit(1)

    target_dir = sys.argv[1]

    if not os.path.exists(target_dir):
        print(f"目录不存在: {target_dir}")
        sys.exit(1)

    # 检查是否在git仓库中
    # if not os.path.exists(os.path.join(target_dir, ".git")):
    #     print(f"目录不是git仓库: {target_dir}")
    #     sys.exit(1)

    merger = DiffBasedMerger(target_dir)
    merger.process_all_files()


if __name__ == "__main__":
    main()
