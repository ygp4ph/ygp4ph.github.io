import requests
import re
from bs4 import BeautifulSoup
import sys

# Since bs4 is not installed, we use simple regex
def get_title(url):
    try:
        # User agent to avoid 403s
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            content = response.text
            match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE | re.DOTALL)
            if match:
                title = match.group(1).strip()
                # Clean up title (decode HTML entities manually or simplistic)
                title = title.replace('&ndash;', '-').replace('&#8211;', '-').replace('&nbsp;', ' ').replace('|', '-')
                # Remove newlines
                title = " ".join(title.split())
                return title
    except Exception as e:
        pass
    return url # Fallback

def main():
    urls = [
        "https://www.verylazytech.com/network-pentesting/ipsec-ike-vpn-port-500-udp",
        "https://angelica.gitbook.io/hacktricks/network-services-pentesting/ipsec-ike-vpn-pentesting",
        "https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/XSLT%20Injection",
        "https://ine.com/blog/xslt-injections-for-dummies",
        "https://www.revshells.com/",
        "https://portswigger.net/web-security/file-upload",
        "https://www.vaadata.com/blog/file-upload-vulnerabilities-and-security-best-practices/",
        "https://projectdiscovery.io/blog/nextjs-middleware-authorization-bypass",
        "https://projectdiscovery.io/blog/nextjs-middleware-authorization-bypass#for-versions-1320-and-later",
        "https://nextjs.org/docs/app/getting-started/project-structure",
        "https://www.jwt.io/",
        "https://nextjs.org/docs/app/getting-started/project-structure#nested-routes",
        "https://nextjs.org/docs/app/getting-started/layouts-and-pages",
        "https://developer.hashicorp.com/terraform/cli/commands/apply",
        "https://developer.hashicorp.com/terraform/cli/config/config-file",
        "https://stackoverflow.com/questions/73815171/execute-bash-script-on-ubutnu-using-terraform",
        "https://medium.com/@saintlafi/linux-privilege-escalation-for-oscp-and-beyond-cheat-sheet-24fb9fe13058",
        # Trickster links to verify consistency
        "https://github.com/0xDTC/Prestashop-CVE-2024-34716",
        "https://github.com/arthaud/git-dumper",
        "https://github.com/aelmokhtar/CVE-2024-34716",
        "https://github.com/s0ck3t-s3c/CVE-2024-32651-changedetection-RCE"
    ]
    
    print("Fetching titles...")
    for url in urls:
        print(f"URL: {url}")
        print(f"TITLE: {get_title(url)}")
        print("---")

if __name__ == "__main__":
    main()
