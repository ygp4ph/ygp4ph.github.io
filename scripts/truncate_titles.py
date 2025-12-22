
import os
import re

def truncate_text(text, limit=57):
    text = text.strip()
    if len(text) > limit:
        return text[:limit-3] + "..."
    return text

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex to find link integrations:
    # <p class="link-integration"> ... <a href="...">TEXT</a> ... </p>
    # We want to capture the text inside the <a> tag.
    
    # This regex looks for the link-integration paragraph, then the img, then the a tag.
    # It captures the A tag content in group 3.
    pattern = re.compile(r'(<p class="link-integration">\s*<img[^>]*>\s*<a href="[^"]*"[^>]*>)(.*?)(</a>\s*</p>)', re.DOTALL)

    def replace_match(match):
        prefix = match.group(1)
        text = match.group(2)
        suffix = match.group(3)
        
        new_text = truncate_text(text)
        
        if new_text != text:
             print(f"Truncating: {text[:20]}... -> {new_text}")
             
        return f"{prefix}{new_text}{suffix}"

    new_content = pattern.sub(replace_match, content)

    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {file_path}")

def main():
    writeups_dir = "/home/ygp4ph/Projets/ygp4ph.github.io/writeups"
    for root, dirs, files in os.walk(writeups_dir):
        for file in files:
            if file.endswith(".html"):
                process_file(os.path.join(root, file))

if __name__ == "__main__":
    main()
