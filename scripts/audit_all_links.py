import os
import re

WRITEUPS_DIR = "/home/ygp4ph/Projets/ygp4ph.github.io/writeups"

def analyze_links():
    print(f"Scanning {WRITEUPS_DIR}...\n")
    
    integration_pattern = re.compile(r'<p class="link-integration">.*?</p>', re.DOTALL)
    a_tag_pattern = re.compile(r'<a\s+[^>]*href="([^"]+)"[^>]*>(.*?)</a>', re.DOTALL)

    for root, dirs, files in os.walk(WRITEUPS_DIR):
        for file in files:
            if file.endswith(".html"):
                filepath = os.path.join(root, file)
                relpath = os.path.relpath(filepath, WRITEUPS_DIR)
                
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()

                # Map integrated hrefs
                integrated_blocks = integration_pattern.findall(content)
                integrated_hrefs = []
                for block in integrated_blocks:
                    match = a_tag_pattern.search(block)
                    if match:
                        integrated_hrefs.append(match.group(1))

                all_links = a_tag_pattern.findall(content)
                if not all_links:
                    continue

                for href, text in all_links:
                    if not href.startswith("http"):
                        continue
                    if any(x in href for x in ["w3.org", "fonts.google", "localhost", "127.0.0.1"]):
                        continue
                        
                    clean_text = re.sub(r'\s+', '', text).strip()
                    clean_href = href.strip()
                    
                    # Check if text looks like the URL
                    is_url_text = (clean_text == clean_href) or (clean_text in clean_href) or (clean_href in clean_text)
                    
                    status = "UNKNOWN"
                    if href in integrated_hrefs:
                        if is_url_text:
                            status = "INTEGRATED-BAD-TITLE"
                        else:
                            status = "INTEGRATED-OK"
                    else:
                        if is_url_text:
                            status = "CANDIDATE-BAD-TITLE"
                        else:
                            status = "INLINE-OK" # Assuming manually named links are fine
                    
                    if "BAD-TITLE" in status or status == "CANDIDATE-BAD-TITLE":
                        print(f"File: {relpath}")
                        print(f"  [{status}] {href}")
                        print(f"  Text: {text[:50]}...")
                        print("")

if __name__ == "__main__":
    analyze_links()
