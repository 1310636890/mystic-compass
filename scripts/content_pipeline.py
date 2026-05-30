#!/usr/bin/env python3
"""
Mystic Compass End-to-End Content Pipeline
===========================================
Reads data/article_knowledge.yaml → generates complete Hugo .md articles
with real content (not placeholders), tool CTAs, affiliate disclosures,
and internal cross-links.

Usage:
  python scripts/content_pipeline.py              # generate all
  python scripts/content_pipeline.py --dry-run     # preview only
  python scripts/content_pipeline.py --slug feng-shui-for-beginners
"""

import yaml
import os
import sys
import argparse
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(ROOT, "data", "article_knowledge.yaml")
CONTENT_DIR = os.path.join(ROOT, "content")

# === TEMPLATES ===

ARTICLE_START = """---
title: "{title}"
description: "{description}"
date: {date}
draft: false
type: blog
---

<div style="padding:2rem;background:linear-gradient(135deg,rgba(212,165,116,0.12),rgba(212,165,116,0.05));border-radius:12px;border:1px solid rgba(212,165,116,0.2);text-align:center;margin:2rem 0;">
  <h2 style="color:#d4a574;margin-bottom:0.5rem;">Try Our Free {tool_name} First</h2>
  <p style="color:#aaa;margin-bottom:1rem;">{tool_cta}</p>
  <a href="{target_tool}" style="display:inline-block;padding:0.8rem 2rem;background:#d4a574;color:#1a1a2e;text-decoration:none;border-radius:8px;font-weight:bold;">Launch Free Tool →</a>
</div>

"""

ARTICLE_END = """
<div style="text-align:center;margin:2.5rem 0;padding:2rem;background:linear-gradient(135deg,rgba(212,165,116,0.12),rgba(212,165,116,0.05));border-radius:12px;border:1px solid rgba(212,165,116,0.2);">
  <h2 style="color:#d4a574;">Get Your Personal {tool_name} Results</h2>
  <p style="color:#aaa;margin-bottom:1rem;">Stop guessing. Use our free tools to get results tailored to your space.</p>
  <a href="/tools/" style="display:inline-block;padding:0.8rem 2rem;background:#d4a574;color:#1a1a2e;text-decoration:none;border-radius:8px;font-weight:bold;">Browse All Free Tools →</a>
</div>

<div style="margin:2rem 0;padding:1.5rem;background:rgba(212,165,116,0.06);border-radius:10px;border:1px solid rgba(212,165,116,0.15);">
  <h3 style="color:#d4a574;">Recommended Products</h3>
  <p style="color:#999;font-size:0.9rem;">Based on the principles in this guide. <em>We may earn a commission at no extra cost to you.</em></p>
  <table style="width:100%;border-collapse:collapse;margin-top:1rem;">
    <tr style="border-bottom:1px solid rgba(212,165,116,0.15);">
      <td style="padding:0.5rem;font-weight:600;color:#d4a574;">Feng Shui Mall</td>
      <td style="padding:0.5rem;color:#aaa;">Crystals, compasses, fountains — 10% commission, 180-day cookie</td>
      <td style="padding:0.5rem;text-align:right;"><a href="https://www.fengshuimall.com/?ref=mysticcompass" target="_blank" rel="nofollow sponsored" style="display:inline-block;padding:0.3rem 0.8rem;background:#d4a574;color:#1a1a2e;text-decoration:none;border-radius:6px;font-weight:bold;font-size:0.85rem;">Visit Store</a></td>
    </tr>
    <tr>
      <td style="padding:0.5rem;font-weight:600;color:#d4a574;">Feng Shui Import</td>
      <td style="padding:0.5rem;color:#aaa;">Books, calendars, amulets — US-based, worldwide shipping</td>
      <td style="padding:0.5rem;text-align:right;"><a href="https://www.fengshui-import.com/?ref=mysticcompass" target="_blank" rel="nofollow sponsored" style="display:inline-block;padding:0.3rem 0.8rem;background:#d4a574;color:#1a1a2e;text-decoration:none;border-radius:6px;font-weight:bold;font-size:0.85rem;">Visit Store</a></td>
    </tr>
  </table>
</div>

<div style="text-align:center;margin-top:2rem;padding:1rem;background:rgba(212,165,116,0.05);border-radius:8px;font-size:0.85rem;color:#777;">
  <strong>Affiliate Disclosure:</strong> We may earn a commission at no cost to you. This keeps our tools free.<br>
  See our <a href="/best/feng-shui-products-home/" style="color:#d4a574;">recommended Feng Shui products</a>.
</div>
"""


def de_ai(text):
    """Apply anti-AI-slop rules to clean generated text."""
    # Remove common AI-ism opening phrases
    ai_openings = [
        "In today's rapidly evolving",
        "In the ever-changing landscape of",
        "As we navigate the complexities of",
        "It is important to note that",
        "It's worth mentioning that",
        "Furthermore,",
        "Moreover,",
        "Additionally,",
        "In conclusion,",
        "To sum up,",
        "Needless to say,",
        "It goes without saying that",
        "In other words,",
        "As a matter of fact,",
    ]
    for phrase in ai_openings:
        if text.startswith(phrase):
            text = text[len(phrase):].strip()

    # Remove "In order to" → "To"
    text = text.replace("In order to ", "To ")
    text = text.replace("in order to ", "to ")

    # Remove excessive hedging
    hedges = [
        "It could potentially be argued that",
        "Some might say that",
        "It is generally believed that",
    ]
    for h in hedges:
        text = text.replace(h, "")

    # Clean up double spaces
    while "  " in text:
        text = text.replace("  ", " ")

    return text.strip()


def generate_article(article, dry_run=False):
    """Generate a complete blog article from knowledge data."""
    slug = article["slug"]
    today = str(date.today())

    # Build header
    header = ARTICLE_START.format(
        title=article["title"],
        description=article["description"],
        date=today,
        tool_name=article.get("tool_name", "Feng Shui Tools"),
        tool_cta=article.get("tool_cta", ""),
        target_tool=article.get("target_tool", "/tools/"),
    )

    # Build body from sections
    body_parts = []
    for section in article.get("sections", []):
        heading = section["heading"]
        content = section.get("content", "").strip()

        # De-AI the content
        # Split into paragraphs, clean each
        paragraphs = content.split("\n\n")
        cleaned_paras = []
        for para in paragraphs:
            para = para.strip()
            if para:
                para = de_ai(para)
                cleaned_paras.append(para)

        content = "\n\n".join(cleaned_paras)

        # Add facts as blockquote if present
        facts = section.get("facts", [])
        facts_block = ""
        if facts:
            facts_block = '\n\n<div style="padding:1rem 1.5rem;background:rgba(212,165,116,0.06);border-left:3px solid #d4a574;margin:1.5rem 0;border-radius:0 8px 8px 0;">\n'
            for fact in facts:
                facts_block += f'  <p style="color:#999;font-size:0.85rem;margin:0.3rem 0;">📖 {fact}</p>\n'
            facts_block += '</div>'

        body_parts.append(f"## {heading}\n\n{content}{facts_block}")

    body = "\n\n".join(body_parts)

    # Footer
    footer = ARTICLE_END.format(
        tool_name=article.get("tool_name", "Feng Shui Tools"),
    )

    full_content = header + body + footer

    filepath = os.path.join(CONTENT_DIR, "blog", f"{slug}.md")
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    if dry_run:
        word_count = len(full_content.split())
        print(f"[DRY RUN] Would create: {filepath}")
        print(f"  Title: {article['title']}")
        print(f"  Keyword: {article.get('keyword')} ({article.get('volume', '?')}/mo)")
        print(f"  Word count: ~{word_count}")
        print(f"  Sections: {len(article.get('sections', []))}")
        return filepath, word_count

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(full_content)

    word_count = len(full_content.split())
    print(f"[GENERATED] {filepath} (~{word_count} words)")
    return filepath, word_count


def main():
    parser = argparse.ArgumentParser(description="Mystic Compass Content Pipeline")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--slug", type=str)
    args = parser.parse_args()

    if not os.path.exists(DATA_FILE):
        print(f"ERROR: {DATA_FILE} not found")
        sys.exit(1)

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    articles = data.get("articles", [])
    total_words = 0
    generated = 0

    print(f"=== Mystic Compass Content Pipeline === {date.today()} ===")
    if args.dry_run:
        print("DRY RUN — no files written\n")

    for article in articles:
        if args.slug and article["slug"] != args.slug:
            continue
        _, words = generate_article(article, dry_run=args.dry_run)
        total_words += words
        generated += 1

    print(f"\n=== Done: {generated} articles, ~{total_words} total words {'(DRY RUN)' if args.dry_run else ''} ===")


if __name__ == "__main__":
    main()
