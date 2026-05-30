#!/usr/bin/env python3
"""
Mystic Compass PSEO Content Generator
======================================
Reads data/seo_content.yaml → generates Hugo .md pages for blog posts, 
FAQ pages, and long-tail guides. Auto-adds tool CTAs, internal links, 
FAQ schema, and affiliate disclosure.

Usage:
  python scripts/pseo_generator.py              # generate all pages
  python scripts/pseo_generator.py --dry-run     # preview without writing
  python scripts/pseo_generator.py --only blog   # only blog posts
  python scripts/pseo_generator.py --slug feng-shui-for-beginners  # single page
"""

import yaml
import os
import sys
import argparse
from datetime import date

# Paths
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(ROOT, "data", "seo_content.yaml")
CONTENT_DIR = os.path.join(ROOT, "content")

# Base template for blog posts
BLOG_TEMPLATE = """---
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

{body}

<div style="text-align:center;margin:2.5rem 0;padding:2rem;background:linear-gradient(135deg,rgba(212,165,116,0.12),rgba(212,165,116,0.05));border-radius:12px;border:1px solid rgba(212,165,116,0.2);">
  <h2 style="color:#d4a574;">Get Your Personal Assessment</h2>
  <p style="color:#aaa;margin-bottom:1rem;">Stop guessing. Use our free {tool_name} to get results tailored to your space.</p>
  <a href="/tools/" style="display:inline-block;padding:0.8rem 2rem;background:#d4a574;color:#1a1a2e;text-decoration:none;border-radius:8px;font-weight:bold;">Browse Free Tools →</a>
</div>

<div style="text-align:center;margin-top:2rem;padding:1rem;background:rgba(212,165,116,0.05);border-radius:8px;font-size:0.85rem;color:#777;">
  <strong>Affiliate Disclosure:</strong> We may earn a commission when you purchase through our links — at no cost to you.<br>
  See our <a href="/best/feng-shui-products-home/" style="color:#d4a574;">recommended Feng Shui products</a>.
</div>
"""

# Tool name mappings
TOOL_NAMES = {
    "/tools/kua-number-calculator/": "Kua Number Calculator",
    "/tools/flying-star-chart/": "Flying Star Chart",
    "/tools/bagua-map-overlay/": "Bagua Map Overlay",
}

TOOL_CTAS = {
    "/tools/kua-number-calculator/": "Find your personal Kua number, lucky directions, and ideal colors — in 10 seconds.",
    "/tools/flying-star-chart/": "See which sectors of your home bring wealth, illness, or opportunity in 2026.",
    "/tools/bagua-map-overlay/": "Map the 8 life areas onto your floor plan. Find exactly where to place everything.",
}


def generate_blog_post(topic, dry_run=False):
    """Generate a single blog post from topic data."""
    slug = topic["slug"]
    target_tool = topic.get("target_tool", "/tools/")
    tool_name = TOOL_NAMES.get(target_tool, "Feng Shui Tools")
    tool_cta = TOOL_CTAS.get(target_tool, "Use our free tools to assess your Feng Shui.")

    # Build body from sections
    sections = topic.get("sections", [])
    body_parts = []
    for section in sections:
        heading = section.get("heading", "")
        body_parts.append(f"## {heading}\n\n[Content for: {heading} — to be written]\n")

    body = "\n".join(body_parts)

    content = BLOG_TEMPLATE.format(
        title=topic["title"],
        description=topic["description"],
        date=str(date.today()),
        target_tool=target_tool,
        tool_name=tool_name,
        tool_cta=tool_cta,
        body=body.strip(),
    )

    filepath = os.path.join(CONTENT_DIR, "blog", f"{slug}.md")
    
    if dry_run:
        print(f"[DRY RUN] Would create: {filepath}")
        print(f"  Title: {topic['title']}")
        print(f"  Keyword: {topic.get('keyword')} ({topic.get('volume', '?')}/mo)")
        return

    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[CREATED] {filepath}")


def generate_faq_page(faq_group, dry_run=False):
    """Generate a FAQ page with schema markup for a tool page."""
    tool_page = faq_group.get("target_page", "")
    tool_slug = tool_page.strip("/").split("/")[-1]
    questions = faq_group.get("questions", [])

    if not questions:
        return

    # Build FAQ schema JSON-LD
    faq_items = []
    for qa in questions:
        faq_items.append(f"""    {{
      "@type": "Question",
      "name": "{qa['q']}",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "{qa['a']}"
      }}
    }}""")

    schema_block = f"""<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
{',\n'.join(faq_items)}
  ]
}}
</script>"""

    if dry_run:
        print(f"[DRY RUN] FAQ schema for: {tool_page} ({len(questions)} questions)")
        return

    # Find the tool page and inject FAQ schema
    tool_file = os.path.join(CONTENT_DIR, "tools", f"{tool_slug}.md")
    if not os.path.exists(tool_file):
        print(f"[SKIP] Tool page not found: {tool_file}")
        return

    with open(tool_file, "r", encoding="utf-8") as f:
        original = f.read()

    # Only inject if not already present
    if "FAQPage" in original:
        print(f"[SKIP] FAQ schema already exists in {tool_file}")
        return

    # Inject schema after frontmatter (after second ---)
    parts = original.split("---", 2)
    if len(parts) >= 3:
        new_content = "---".join(parts[:2]) + "---\n\n" + schema_block + "\n" + parts[2]
    else:
        new_content = original + "\n\n" + schema_block

    with open(tool_file, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"[INJECTED] FAQ schema into {tool_file}")


def main():
    parser = argparse.ArgumentParser(description="Mystic Compass PSEO Content Generator")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing files")
    parser.add_argument("--only", choices=["blog", "faq", "guides"], help="Generate only one content type")
    parser.add_argument("--slug", type=str, help="Generate only a specific page by slug")
    args = parser.parse_args()

    # Load data
    if not os.path.exists(DATA_FILE):
        print(f"ERROR: Data file not found: {DATA_FILE}")
        sys.exit(1)

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    today = str(date.today())
    print(f"=== Mystic Compass PSEO Generator === {today} ===")
    
    if args.dry_run:
        print("DRY RUN MODE — no files will be written\n")

    # Generate blog posts
    if not args.only or args.only == "blog":
        print("\n--- Blog Posts ---")
        for topic in data.get("blog_topics", []):
            if args.slug and topic["slug"] != args.slug:
                continue
            generate_blog_post(topic, dry_run=args.dry_run)

    # Generate FAQ schema injection
    if not args.only or args.only == "faq":
        print("\n--- FAQ Schema Injection ---")
        for faq_group in data.get("faq_groups", []):
            generate_faq_page(faq_group, dry_run=args.dry_run)

    # Generate guide pages
    if not args.only or args.only == "guides":
        print("\n--- Guide Pages ---")
        for guide in data.get("guide_pages", []):
            if args.slug and guide["slug"] != args.slug:
                continue
            # Guides use the same template as blogs for now
            guide["sections"] = [{"heading": guide.get("keyword", "")}]
            generate_blog_post(guide, dry_run=args.dry_run)
            # Move generated file from blog to guide directory
            blog_path = os.path.join(CONTENT_DIR, "blog", f"{guide['slug']}.md")
            guide_path = os.path.join(CONTENT_DIR, "guide", f"{guide['slug']}.md")
            if not args.dry_run and os.path.exists(blog_path):
                os.makedirs(os.path.dirname(guide_path), exist_ok=True)
                os.rename(blog_path, guide_path)
                print(f"[MOVED] {blog_path} → {guide_path}")

    print(f"\n=== Done {'(DRY RUN)' if args.dry_run else ''} ===")


if __name__ == "__main__":
    main()
