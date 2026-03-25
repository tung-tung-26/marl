#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from pathlib import Path

# 支持的文件扩展名（按需修改）
SUPPORTED_EXTENSIONS = {'.py', 'md', '.txt', '.mo'}

# 默认排除的目录（包括隐藏目录和常见构建目录）
EXCLUDE_DIRS = {
    '.git', '__pycache__', '.venv', 'venv', 'node_modules',
    '.idea', '.vscode', '.mypy_cache', '.pytest_cache',
    'build', 'dist', 'logs', '.DS_Store', 'exps'
}


def should_include_file(file_path: Path) -> bool:
    # 排除自身脚本（避免导出自己）
    if file_path.name == "export_code_to_md.py":
        return False

    # 检查路径中是否包含排除目录
    try:
        parts = file_path.relative_to(Path.cwd()).parts
    except ValueError:
        return False

    for part in parts:
        if part in EXCLUDE_DIRS or part.startswith('.'):
            return False

    # 检查扩展名
    return file_path.suffix.lower() in SUPPORTED_EXTENSIONS


def safe_read_file(file_path: Path, max_size_mb=5) -> str:
    """安全读取文件，跳过大文件和二进制文件"""
    try:
        # 跳过大文件（默认 >5MB）
        if file_path.stat().st_size > max_size_mb * 1024 * 1024:
            return f"⚠️ Skipped: file too large (> {max_size_mb} MB)\n"

        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            return f.read()
    except (OSError, UnicodeDecodeError, PermissionError) as e:
        return f"⚠️ Skipped: {type(e).__name__}: {e}\n"


def main(output_file="project_code.md"):
    root = Path.cwd()
    output_path = root / output_file

    print(f"🔍 Scanning project files in: {root}")

    # 使用 os.walk 避免 symlink 死循环（更安全）
    all_files = []
    for dirpath, dirnames, filenames in os.walk(root, topdown=True):
        # 修改 dirnames 原地排除目录（防止进入）
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS and not d.startswith('.')]# and d in ["mympc"]]#  not in ["archive", "runs", "simulink", "test"]]

        for filename in filenames:
            file_path = Path(dirpath) / filename
            if should_include_file(file_path):
                all_files.append(file_path)

    all_files.sort()
    print(f"✅ Found {len(all_files)} files to export.")

    with open(output_path, 'w', encoding='utf-8') as md:
        for i, file_path in enumerate(all_files, 1):
            rel_path = file_path.relative_to(root)
            depth = len(rel_path.parts)
            h_level = min(6, max(2, depth + 1))  # 根文件为 ##，子目录更深则用 ### 等
            md.write(f"{'#' * h_level} `{rel_path}`\n\n")

            content = safe_read_file(file_path)
            ext = file_path.suffix.lstrip('.').lower()
            lang = ext if ext in {'py', 'js', 'ts', 'jsx', 'tsx', 'html', 'css', 'json', 'yaml', 'yml', 'md',
                                  'txt'} else ''
            md.write(f"```{lang}\n{content}\n```\n\n")

            # 打印进度（避免“卡住”错觉）
            if i % 10 == 0:
                print(f"   Processed {i}/{len(all_files)} files...")

    print(f"🎉 Done! Output saved to: {output_path}")


if __name__ == "__main__":
    main()
