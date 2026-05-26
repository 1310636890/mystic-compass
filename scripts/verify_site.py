"""
verify_site.py — 轻量验证脚本。curl 检查页面状态，不用 browser。
相比 browser_navigate（每次 2-5K tokens），curl 只需几十字符。

用法:
  python scripts/verify_site.py                    # 检查所有关键页面
  python scripts/verify_site.py --url /reviews/    # 检查特定路径
  python scripts/verify_site.py --sitemap          # 从 sitemap 验证
"""

import urllib.request
import urllib.error
import sys
import time
from pathlib import Path

BASE_URL = "https://like-chess.surge.sh"
TIMEOUT = 10

CRITICAL_PAGES = [
    "/",                                          # 首页
    "/reviews/fengshui-world/",                   # 最高佣金 review
    "/reviews/joey-yap/",                         # 最高流量 review
    "/best/feng-shui-courses-beginners/",         # Money page
    "/best/feng-shui-products-home/",             # Money page
    "/guide/feng-shui-bagua-map-guide/",          # 最长 guide
    "/affiliate-programs/",                       # B2B 专区
]

def check(url, label=""):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'MysticCompass/1.0'})
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            status = resp.status
            size = len(resp.read())
            return True, status, size
    except urllib.error.HTTPError as e:
        return False, e.code, 0
    except Exception as e:
        return False, str(e), 0

def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('--url', help='Check specific URL path (e.g., /reviews/)')
    ap.add_argument('--sitemap', action='store_true', help='Check all pages from sitemap')
    args = ap.parse_args()

    urls = CRITICAL_PAGES if not args.url else [args.url]
    
    ok = fail = 0
    for path in urls:
        url = BASE_URL + path
        label = path.rstrip('/').split('/')[-1] or 'home'
        success, status, size = check(url, label)
        if success:
            print(f"  ✅ {path:50s} {status} {size:>6,}B")
            ok += 1
        else:
            print(f"  ❌ {path:50s} {status}")
            fail += 1
        time.sleep(0.3)  # rate limit

    print(f"\n{'✅ All passed' if fail == 0 else f'⚠️  {fail}/{ok+fail} failed'}")

if __name__ == '__main__':
    main()
