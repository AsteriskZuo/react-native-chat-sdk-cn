#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import subprocess
import sys
from pathlib import Path
from typing import List, Tuple, Dict


class GitDiffParser:
    def __init__(self, source_dir: str, target_dir: str):
        self.source_dir = Path(source_dir)
        self.target_dir = Path(target_dir)

    def get_git_diff(self, file_path: str) -> str:
        """获取指定文件的git diff输出"""
        try:
            cmd = [
                "git",
                "diff",
                "--no-index",
                "--no-prefix",
                str(self.target_dir / file_path),
                str(self.source_dir / file_path),
            ]
            result = subprocess.run(
                cmd, capture_output=True, text=True, cwd=self.target_dir
            )
            return result.stdout
        except Exception as e:
            print(f"获取diff失败 {file_path}: {e}")
            return ""

    def parse_diff_chunks(self, diff_content: str) -> List[Dict]:
        """解析diff内容，提取变更块"""
        chunks = []
        lines = diff_content.split("\n")

        i = 0
        while i < len(lines):
            line = lines[i]

            # 找到变更块头部 (@@开头)
            if line.startswith("@@"):
                chunk_header = line
                chunk_lines = []
                i += 1

                # 收集这个块的所有行
                while i < len(lines) and not lines[i].startswith("@@"):
                    chunk_lines.append(lines[i])
                    i += 1

                chunks.append({"header": chunk_header, "lines": chunk_lines})
                continue
            i += 1

        return chunks

    def analyze_chunk(self, chunk_lines: List[str]) -> str:
        """分析变更块类型"""
        removed_lines = [line[1:] for line in chunk_lines if line.startswith("-")]
        added_lines = [line[1:] for line in chunk_lines if line.startswith("+")]
        context_lines = [line[1:] for line in chunk_lines if line.startswith(" ")]

        # 如果没有删除和新增，是上下文
        if not removed_lines and not added_lines:
            return "context"

        # 如果只有新增，没有删除，是纯新增
        if added_lines and not removed_lines:
            return "pure_addition"

        # 如果只有删除，没有新增，是纯删除
        if removed_lines and not added_lines:
            return "pure_deletion"

        # 判断是否为纯注释变更（中英文互译）
        if self.is_comment_translation(removed_lines, added_lines):
            return "comment_translation"

        # 其他情况为复杂变更
        return "complex_change"

    def is_comment_translation(
        self, removed_lines: List[str], added_lines: List[str]
    ) -> bool:
        """判断是否为注释的中英文互译"""

        # 检查是否都是注释行
        def is_comment_block(lines):
            comment_patterns = [
                r"^\s*/\*\*?",  # /** 或 /*
                r"^\s*\*",  # *
                r"^\s*\*/",  # */
                r"^\s*//",  # //
            ]

            for line in lines:
                line = line.strip()
                if not line:  # 空行
                    continue

                is_comment = any(
                    re.match(pattern, line) for pattern in comment_patterns
                )
                if not is_comment:
                    return False
            return True

        # 检查是否包含中文
        def has_chinese(text):
            return bool(re.search(r"[\u4e00-\u9fff]", text))

        # 检查是否包含英文单词
        def has_english_words(text):
            return bool(re.search(r"[a-zA-Z]{2,}", text))

        if not is_comment_block(removed_lines) or not is_comment_block(added_lines):
            return False

        removed_text = " ".join(removed_lines)
        added_text = " ".join(added_lines)

        # 删除的是中文注释，新增的是英文注释
        return has_chinese(removed_text) and has_english_words(added_text)

    def merge_chunk(self, chunk_lines: List[str], chunk_type: str) -> List[str]:
        """根据块类型进行合并"""
        if chunk_type == "context":
            # 上下文行直接保留
            return [line[1:] for line in chunk_lines if line.startswith(" ")]

        elif chunk_type == "pure_addition":
            # 纯新增：采用新版本
            context_lines = [line[1:] for line in chunk_lines if line.startswith(" ")]
            added_lines = [line[1:] for line in chunk_lines if line.startswith("+")]
            return context_lines + added_lines

        elif chunk_type == "pure_deletion":
            # 纯删除：保留原版本
            return [line[1:] for line in chunk_lines if line.startswith("-")]

        elif chunk_type == "comment_translation":
            # 注释翻译：保留中文注释
            context_lines = [line[1:] for line in chunk_lines if line.startswith(" ")]
            removed_lines = [line[1:] for line in chunk_lines if line.startswith("-")]
            return context_lines + removed_lines

        else:  # complex_change
            # 复杂变更：保留原版本并添加标记
            result = []
            result.append("// TODO: MANUAL_MERGE_REQUIRED - 需要人工合并")
            result.append("// 原始版本和新版本都有复杂变更，请手动检查")

            # 保留原版本
            for line in chunk_lines:
                if line.startswith(" "):
                    result.append(line[1:])
                elif line.startswith("-"):
                    result.append(line[1:])

            return result

    def merge_file(self, file_path: str) -> Tuple[bool, str]:
        """合并单个文件"""
        diff_content = self.get_git_diff(file_path)

        if not diff_content:
            # 没有差异，直接复制源文件
            return True, "no_diff"

        # 读取目标文件内容
        target_file = self.target_dir / file_path
        if not target_file.exists():
            # 目标文件不存在，直接复制源文件
            return True, "new_file"

        # 解析diff
        chunks = self.parse_diff_chunks(diff_content)
        if not chunks:
            return True, "no_chunks"

        # 读取原文件内容
        with open(target_file, "r", encoding="utf-8") as f:
            original_lines = f.readlines()

        # 逐块处理并重建文件
        merged_content = self.rebuild_file_from_chunks(original_lines, chunks)

        # 写入合并后的内容
        with open(target_file, "w", encoding="utf-8") as f:
            f.write(merged_content)

        return True, "merged"

    def rebuild_file_from_chunks(
        self, original_lines: List[str], chunks: List[Dict]
    ) -> str:
        """从chunks重建文件内容"""
        result_lines = []
        last_end = 0

        for chunk in chunks:
            # 解析chunk header获取行号信息
            header = chunk["header"]
            match = re.search(
                r"@@\s*-(\d+)(?:,(\d+))?\s*\+(\d+)(?:,(\d+))?\s*@@", header
            )
            if not match:
                continue

            old_start = int(match.group(1)) - 1  # 转为0索引
            old_count = int(match.group(2)) if match.group(2) else 1

            # 添加chunk之前的原始内容
            if old_start > last_end:
                result_lines.extend(original_lines[last_end:old_start])

            # 分析并合并当前chunk
            chunk_type = self.analyze_chunk(chunk["lines"])
            merged_lines = self.merge_chunk(chunk["lines"], chunk_type)

            # 确保行末有换行符
            for line in merged_lines:
                if not line.endswith("\n"):
                    line += "\n"
                result_lines.append(line)

            last_end = old_start + old_count

        # 添加文件末尾的原始内容
        if last_end < len(original_lines):
            result_lines.extend(original_lines[last_end:])

        return "".join(result_lines)

    def get_typescript_files(self, directory: Path) -> List[str]:
        """递归获取所有TypeScript文件"""
        ts_files = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(".ts") or file.endswith(".tsx"):
                    rel_path = os.path.relpath(os.path.join(root, file), directory)
                    ts_files.append(rel_path)
        return ts_files

    def smart_merge_all(self):
        """智能合并所有TypeScript文件"""
        print("开始智能合并...")

        # 获取源目录中的所有TypeScript文件
        source_ts_files = self.get_typescript_files(self.source_dir)
        target_ts_files = self.get_typescript_files(self.target_dir)

        # 合并文件列表
        all_files = set(source_ts_files + target_ts_files)

        success_count = 0
        total_count = len(all_files)

        results = {"merged": [], "no_diff": [], "new_file": [], "error": []}

        for file_path in sorted(all_files):
            try:
                print(f"处理文件: {file_path}")

                # 检查源文件是否存在
                source_file = self.source_dir / file_path
                target_file = self.target_dir / file_path

                if source_file.exists() and not target_file.exists():
                    # 新文件，直接复制
                    target_file.parent.mkdir(parents=True, exist_ok=True)
                    import shutil

                    shutil.copy2(source_file, target_file)
                    results["new_file"].append(file_path)
                    success_count += 1
                elif source_file.exists() and target_file.exists():
                    # 合并现有文件
                    success, result_type = self.merge_file(file_path)
                    if success:
                        results[result_type].append(file_path)
                        success_count += 1
                    else:
                        results["error"].append(file_path)
                else:
                    # 文件在目标目录存在但源目录不存在，删除目标文件
                    if target_file.exists():
                        target_file.unlink()
                        results["deleted"] = results.get("deleted", [])
                        results["deleted"].append(file_path)
                        print(f"  已删除文件: {file_path}")
                        success_count += 1
                    else:
                        results["no_diff"].append(file_path)
                        success_count += 1

            except Exception as e:
                print(f"处理文件 {file_path} 时出错: {e}")
                results["error"].append(file_path)

        # 输出处理结果
        print(f"\n=== 处理完成 ===")
        print(f"总文件数: {total_count}")
        print(f"成功处理: {success_count}")
        print(f"失败: {len(results['error'])}")
        print(f"\n详细结果:")
        print(f"  - 智能合并: {len(results['merged'])} 个文件")
        print(f"  - 无差异: {len(results['no_diff'])} 个文件")
        print(f"  - 新文件: {len(results['new_file'])} 个文件")
        print(f"  - 错误: {len(results['error'])} 个文件")

        if results["error"]:
            print(f"\n错误文件列表:")
            for file in results["error"]:
                print(f"  - {file}")


def main():
    if len(sys.argv) != 3:
        print("用法: python smart_merge.py <源目录> <目标目录>")
        print("示例: python smart_merge.py /path/to/source /path/to/target")
        sys.exit(1)

    source_dir = sys.argv[1]
    target_dir = sys.argv[2]

    if not os.path.exists(source_dir):
        print(f"源目录不存在: {source_dir}")
        sys.exit(1)

    if not os.path.exists(target_dir):
        print(f"目标目录不存在: {target_dir}")
        sys.exit(1)

    merger = GitDiffParser(source_dir, target_dir)
    merger.smart_merge_all()


if __name__ == "__main__":
    main()
