#!/usr/bin/env python3
"""
Mystic Compass Daily Content Publisher
======================================
AI writes content (in article_knowledge.yaml) — script handles the rest:
  1. Pick next unpublished article
  2. Generate Hugo .md via content_pipeline
  3. Mark as published
  4. Optionally git commit + push

Usage:
  python scripts/daily_publish.py                    # generate next article
  python scripts/daily_publish.py --dry-run           # preview which article
  python scripts/daily_publish.py --slug xxx          # publish specific article  
  python scripts/daily_publish.py --commit            # auto git add+commit
  python scripts/daily_publish.py --list              # show publishing queue
  python scripts/daily_publish.py --reset             # reset all published status
"""

import yaml
import os
import sys
import argparse
import subprocess
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(ROOT, "data", "article_knowledge.yaml")
PUBLISHED_FILE = os.path.join(ROOT, "data", "published.yaml")
CONTENT_DIR = os.path.join(ROOT, "content")

# We import and reuse content_pipeline's generate function
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from content_pipeline import generate_article


def load_published():
    with open(PUBLISHED_FILE, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {"published": {}, "total_published": 0}


def save_published(data):
    data["total_published"] = len(data["published"])
    with open(PUBLISHED_FILE, "w", encoding="utf-8") as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)


def get_next_article(all_articles, published: dict):
    """Find the first unpublished article."""
    for article in all_articles:
        if article["slug"] not in published:
            return article
    return None


def list_queue(all_articles, published: dict):
    """Show the publishing queue."""
    print("\n=== Publishing Queue ===")
    done = 0
    pending = 0
    for i, article in enumerate(all_articles):
        slug = article["slug"]
        status = "✅ PUBLISHED" if slug in published else "⏳ PENDING"
        pub_date = published.get(slug, "")
        kw = article.get("keyword", "")
        vol = article.get("volume", "?")
        print(f"  [{i+1:2d}] {status:14s} {slug:45s} | {kw} ({vol}/mo) {pub_date}")
        if slug in published:
            done += 1
        else:
            pending += 1
    print(f"\n  Published: {done} | Pending: {pending} | Total: {len(all_articles)}\n")


def git_commit_and_push(slug):
    """Automatically git add, commit, and push."""
    try:
        subprocess.run(["git", "add", "-A"], cwd=ROOT, check=True, capture_output=True)
        subprocess.run(
            ["git", "commit", "-m", f"Daily: publish {slug}"],
            cwd=ROOT, check=True, capture_output=True
        )
        print(f"[GIT] Committed: {slug}")
        
        result = subprocess.run(
            ["git", "push", "origin", "main"],
            cwd=ROOT, check=False, capture_output=True, text=True, timeout=60
        )
        if result.returncode == 0:
            print("[GIT] Pushed to GitHub → GitHub Actions deploying to Surge")
        else:
            print(f"[GIT] Push failed — run 'git push' manually:\n{result.stderr}")
    except subprocess.CalledProcessError as e:
        print(f"[GIT] Error: {e.stderr.decode() if e.stderr else str(e)}")


def reset_all(all_articles):
    """Reset all published tracking."""
    data = {"published": {}, "total_published": 0, "next_index": 0}
    save_published(data)
    print(f"Reset: 0/{len(all_articles)} published")


def main():
    parser = argparse.ArgumentParser(description="Mystic Compass Daily Publisher")
    parser.add_argument("--dry-run", action="store_true", help="Preview without generating")
    parser.add_argument("--slug", type=str, help="Publish a specific article")
    parser.add_argument("--commit", action="store_true", help="Auto git add + commit + push")
    parser.add_argument("--list", action="store_true", help="Show publishing queue")
    parser.add_argument("--reset", action="store_true", help="Reset all published status")
    args = parser.parse_args()

    # Load data
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    all_articles = data.get("articles", [])

    pub_data = load_published()
    published = pub_data.get("published", {})

    # Reset
    if args.reset:
        reset_all(all_articles)
        return

    # List
    if args.list:
        list_queue(all_articles, published)
        return

    # Pick article
    if args.slug:
        article = next((a for a in all_articles if a["slug"] == args.slug), None)
        if not article:
            print(f"ERROR: article '{args.slug}' not found in knowledge base")
            sys.exit(1)
    else:
        article = get_next_article(all_articles, published)
        if not article:
            print("ALL ARTICLES PUBLISHED! Add more to data/article_knowledge.yaml")
            return

    slug = article["slug"]
    today = str(date.today())

    print(f"=== Daily Publish: {today} ===")
    print(f"  Article: {slug}")
    print(f"  Keyword: {article.get('keyword')} ({article.get('volume', '?')}/mo)")
    print(f"  Title: {article.get('title')}")

    if args.dry_run:
        print(f"\n[DRY RUN] Would generate: content/blog/{slug}.md")
        return

    # Generate
    filepath, word_count = generate_article(article)
    print(f"  Generated: {filepath} (~{word_count} words)")

    # Mark published
    published[slug] = today
    save_published(pub_data)
    print(f"  Marked published: {slug}")

    # Git commit if requested
    if args.commit:
        git_commit_and_push(slug)

    print(f"\n=== Done: {pub_data['total_published']}/{len(all_articles)} published ===")


if __name__ == "__main__":
    main()
