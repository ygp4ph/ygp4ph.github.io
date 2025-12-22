import os
import re

WRITEUPS_DIR = "/home/ygp4ph/Projets/ygp4ph.github.io/writeups"

def analyze_links():
    print(f"Scanning {WRITEUPS_DIR}...\n")
    
    # Regex to find link integrations
    integration_pattern = re.compile(r'<p class="link-integration">.*?</p>', re.DOTALL)
    
    # Regex to find all 'a' tags
    a_tag_pattern = re.compile(r'<a\s+[^>]*href="([^"]+)"[^>]*>(.*?)</a>', re.DOTALL)

    for root, dirs, files in os.walk(WRITEUPS_DIR):
        for file in files:
            if file.endswith(".html"):
                filepath = os.path.join(root, file)
                relpath = os.path.relpath(filepath, WRITEUPS_DIR)
                
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()

                # Find all integrated links first to exclude them or mark them
                integrated_blocks = integration_pattern.findall(content)
                integrated_hrefs = []
                for block in integrated_blocks:
                    match = a_tag_pattern.search(block)
                    if match:
                        integrated_hrefs.append(match.group(1))

                # Find all links
                all_links = a_tag_pattern.findall(content)
                
                if not all_links:
                    continue

                print(f"File: {relpath}")
                for href, text in all_links:
                    if not href.startswith("http"):
                        continue
                    if "w3.org" in href or "fonts.google" in href or "localhost" in href:
                        continue
                        
                    clean_text = re.sub(r'\s+', ' ', text).strip()
                    
                    if href in integrated_hrefs:
                        status = "INTEGRATED"
                    else:
                        # Simple context check: is the text just the URL?
                        # Or specific keyword check based on user request?
                        if clean_text == href:
                             status = "STANDALONE-CANDIDATE" 
                        else:
                             status = "INLINE"
                    
                    if status != "INTEGRATED":
                         print(f"  [{status}] {href} (Text: '{clean_text[:50]}...')")
                print("")

if __name__ == "__main__":
    analyze_links()
