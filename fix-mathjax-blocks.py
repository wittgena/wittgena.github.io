import os
import re

def convert_display_math(content: str) -> str:
    # 정규식: \[ ... \] 블록을 $$ ... $$로 변경
    pattern = re.compile(r'\\\[\s*([\s\S]+?)\s*\\\]')
    return pattern.sub(r'$$\1$$', content)

def process_file(path: str):
    with open(path, 'r', encoding='utf-8') as f:
        original = f.read()
    converted = convert_display_math(original)
    if original != converted:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(converted)
        print(f"Converted: {path}")
    else:
        print(f"No change: {path}")

def scan_markdown_files(root_dir: str = "."):
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith(".md"):
                filepath = os.path.join(dirpath, filename)
                process_file(filepath)

if __name__ == "__main__":
    print("Scanning for \\[ ... \\] display-math blocks...")
    scan_markdown_files()
    print("Done.")
