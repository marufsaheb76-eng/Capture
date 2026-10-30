#!/usr/bin/env python3

import urllib.request
import urllib.error
from urllib.parse import urlparse
from pathlib import Path
from datetime import datetime
import re

GREEN = "\033[1;32m"
BLUE = "\033[1;34m"
CYAN = "\033[1;36m"
YELLOW = "\033[1;33m"
RED = "\033[1;31m"
BLOOD = "\033[1;38;2;180;0;0m"
RESET = "\033[0m"

BASE = Path.home() / "HTML_CAPTURE"
OUT = BASE / "captured"
DOWNLOADS = Path.home() / "storage" / "downloads"

MAX_SIZE = 10 * 1024 * 1024


def banner():
    print(BLOOD + r"""
██████╗  █████╗ ███╗   ██╗ ██████╗ ███████╗██████╗
██╔══██╗██╔══██╗████╗  ██║██╔════╝ ██╔════╝██╔══██╗
██║  ██║███████║██╔██╗ ██║██║  ███╗█████╗  ██████╔╝
██║  ██║██╔══██║██║╚██╗██║██║   ██║██╔══╝  ██╔══██╗
██████╔╝██║  ██║██║ ╚████║╚██████╔╝███████╗██║  ██║
╚═════╝  ╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝

███╗   ███╗ █████╗ ██████╗ ██╗   ██╗███████╗
████╗ ████║██╔══██╗██╔══██╗██║   ██║██╔════╝
██╔████╔██║███████║██████╔╝██║   ██║█████╗
██║╚██╔╝██║██╔══██╗██╔══██╗██║   ██║██╔══╝
██║ ╚═╝ ██║██║  ██║██║  ██║╚██████╔╝██║

██████╗ ██████╗ ██╗███╗   ███╗███████╗
██╔══██╗██╔══██╗██║████╗ ████║██╔════╝
██████╔╝██████╔╝██║██╔████╔██║█████╗
██╔═══╝ ██╔══██╗██║██║╚██╔╝██║██╔══╝
██║     ██║  ██║██║██║ ╚═╝ ██║███████╗
""" + RESET)

    print(GREEN + "      DANGER MARUF PRIME " + RESET)
    print(BLUE + "=" * 38 + RESET)
    print(CYAN + "       WEBSITE HTML CAPTURER" + RESET)
    print(BLUE + "=" * 38 + RESET)
    print()


def capture():
    url = input(f"{YELLOW}[?] Website URL: {RESET}").strip()

    if not url:
        print(RED + "[!] URL is required." + RESET)
        return

    if not urlparse(url).scheme:
        url = "https://" + url

    parsed = urlparse(url)

    if (
        parsed.scheme not in ("http", "https")
        or not parsed.hostname
        or parsed.username is not None
        or parsed.password is not None
    ):
        print(RED + "[!] Invalid URL." + RESET)
        return

    safe_name = re.sub(r"[^a-zA-Z0-9.-]", "_", parsed.hostname)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    folder = OUT / f"{safe_name}_{stamp}"
    folder.mkdir(parents=True, exist_ok=True)

    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Linux; Android) "
                "AppleWebKit/537.36 Chrome/130.0 "
                "Mobile Safari/537.36"
            )
        }
    )

    try:
        print(CYAN + "\n[+] Connecting to website..." + RESET)

        with urllib.request.urlopen(request, timeout=25) as response:
            content_type = response.headers.get_content_type()

            if content_type not in ("text/html", "application/xhtml+xml"):
                print(RED + f"[!] Not an HTML page: {content_type}" + RESET)
                return

            html = response.read(MAX_SIZE + 1)

            if len(html) > MAX_SIZE:
                print(RED + "[!] HTML exceeds 10 MB limit." + RESET)
                return

            charset = response.headers.get_content_charset() or "utf-8"
            html_text = html.decode(charset, errors="replace")

            file_path = folder / "index.html"
            file_path.write_text(html_text, encoding="utf-8")

            print(GREEN + "\n[+] HTML captured successfully!" + RESET)
            print(CYAN + f"[+] Final URL: {response.geturl()}")
            print(f"[+] Capture: {file_path}")
            print(f"[+] Size: {len(html):,} bytes" + RESET)

            try:
                DOWNLOADS.mkdir(parents=True, exist_ok=True)
                download_path = DOWNLOADS / f"{safe_name}_{stamp}.html"
                download_path.write_text(html_text, encoding="utf-8")
                print(GREEN + f"[+] Phone Storage: {download_path}" + RESET)

            except OSError as e:
                print(YELLOW + f"[!] Downloads save failed: {e}" + RESET)

    except urllib.error.HTTPError as e:
        print(RED + f"[!] HTTP Error: {e.code} {e.reason}" + RESET)

    except urllib.error.URLError as e:
        print(RED + f"[!] Connection Error: {e.reason}" + RESET)

    except TimeoutError:
        print(RED + "[!] Connection timed out." + RESET)

    except Exception as e:
        print(RED + f"[!] Error: {e}" + RESET)


def main():
    OUT.mkdir(parents=True, exist_ok=True)

    while True:
        banner()

        print(GREEN + "[01]" + RESET + " Capture Website HTML")
        print(RED + "[00]" + RESET + " Exit")

        choice = input(f"\n{CYAN}Select option: {RESET}").strip()

        if choice in ("1", "01"):
            capture()
            input("\nPress Enter to continue...")

        elif choice in ("0", "00"):
            print(GREEN + "\nLoneWolf Silent Rush - Goodbye!" + RESET)
            break

        else:
            print(RED + "[!] Invalid option." + RESET)


if __name__ == "__main__":
    main()