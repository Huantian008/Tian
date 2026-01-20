#!/usr/bin/env python3
import os
import re
import chardet
from pathlib import Path

def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        raw_data = f.read()
        if not raw_data:
            return {'encoding': None, 'confidence': 0}
        return chardet.detect(raw_data)

def convert_to_utf8_lf(file_path):
    with open(file_path, 'rb') as f:
        raw_data = f.read()
    
    if not raw_data:
        return False
    
    result = chardet.detect(raw_data)
    encoding = result.get('encoding')
    
    if not encoding:
        try:
            content = raw_data.decode('utf-8', errors='ignore')
        except:
            return False
    else:
        try:
            content = raw_data.decode(encoding)
        except (UnicodeDecodeError, LookupError):
            try:
                content = raw_data.decode('utf-8', errors='ignore')
            except:
                return False
    
    content = content.replace('\r\n', '\n').replace('\r', '\n')
    
    with open(file_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(content)
    
    return True

def has_chinese(text):
    return bool(re.search(r'[\u4e00-\u9fa5]', text))

def add_utf8_pragma(file_path, content):
    lines = content.split('\n')
    
    has_pragma = any('#pragma execution_character_set("utf-8")' in line for line in lines)
    
    if has_pragma or not has_chinese(content):
        return content
    
    insert_pos = 0
    for i, line in enumerate(lines):
        if line.strip().startswith('#include'):
            insert_pos = i + 1
        elif line.strip() and not line.strip().startswith('#'):
            break
    
    if insert_pos > 0:
        lines.insert(insert_pos, '#pragma execution_character_set("utf-8")')
        return '\n'.join(lines)
    
    return content

def remove_chcp(content):
    lines = content.split('\n')
    filtered_lines = []
    for line in lines:
        if 'system(' in line and 'chcp' in line:
            continue
        filtered_lines.append(line)
    return '\n'.join(filtered_lines)

def process_file(file_path):
    if file_path.stat().st_size == 0:
        return
    
    original_encoding = detect_encoding(file_path)
    
    success = convert_to_utf8_lf(file_path)
    
    if not success:
        print(f"跳过: {file_path} (编码检测失败)")
        return
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    content = remove_chcp(content)
    content = add_utf8_pragma(file_path, content)
    
    with open(file_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(content)
    
    enc_info = original_encoding['encoding'] if original_encoding and original_encoding.get('encoding') else 'unknown'
    print(f"已处理: {file_path} ({enc_info} -> UTF-8)")

def main():
    cpp_dir = Path('./cpp')
    
    for ext in ['*.cpp', '*.h', '*.hpp']:
        for file_path in cpp_dir.rglob(ext):
            process_file(file_path)
    
    print("\n所有文件处理完成！")

if __name__ == '__main__':
    main()
