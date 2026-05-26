"""generate_pages.py — YAML to Hugo Markdown Generator v2

Reads data/fengshui_platforms.yaml and generates:
  1. Review pages:      content/reviews/{slug}/index.md
  2. Comparison pages:  content/vs/{s1}-vs-{s2}.md
  3. Best-of pages:     content/best/{category}.md

Usage:
  cd "C:/Users/rjw/Desktop/fengshui-pseo/site/mystic-compass"
  python scripts/generate_pages.py
  python scripts/generate_pages.py --dry-run
  python scripts/generate_pages.py --only reviews

Requires: pip install pyyaml
"""

import yaml
import os
import sys
import argparse
from datetime import date

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(BASE, 'data', 'fengshui_platforms.yaml')
CONTENT = os.path.join(BASE, 'content')


def load_platforms():
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    platforms = data['platforms']
    complete = [p for p in platforms if p.get('data_complete')]
    incomplete = [p for p in platforms if not p.get('data_complete')]
    print(f"Platforms: {len(platforms)} total | Complete: {len(complete)} | Incomplete: {len(incomplete)}")
    if incomplete:
        names = [p['name'] for p in incomplete]
        print(f"  Skipping (incomplete): {', '.join(names)}")
    return platforms


def make_frontmatter(**fields):
    """Build YAML frontmatter string."""
    lines = ['---']
    for k, v in fields.items():
        if v is None:
            continue
        if isinstance(v, str):
            lines.append(f'{k}: "{v}"')
        else:
            lines.append(f'{k}: {v}')
    lines.append('---')
    lines.append('')
    return '\n'.join(lines)


def generate_review(platform, root_dir, today, dry_run=False):
    """Generate a review page."""
    slug = platform['slug']
    page_dir = os.path.join(root_dir, 'reviews', slug)
    page_path = os.path.join(page_dir, 'index.md')

    if not platform.get('data_complete'):
        print(f"  SKIP {slug} (data incomplete)")
        return None

    name = platform['name']
    r = platform['ratings']
    a = platform['affiliate']
    cat = platform.get('category', 'General')

    fm = make_frontmatter(
        title=f"{name} Review {today.year}",
        description=f"Honest {name} review — {r['overall']}/10 rating, {a['commission']}% commission, {a['cookie_days']}d cookie. Pros, cons, pricing, and affiliate program details.",
        date=str(today),
        type="review",
        layout="review",
        slug=slug,
        platform_name=name,
    )

    pros = '\n'.join([f'- {p}' for p in platform.get('pros', [])])
    cons = '\n'.join([f'- {c}' for c in platform.get('cons', [])])
    product_lines = '\n'.join([f'- {pl}' for pl in platform.get('product_lines', [])])
    best_for = '\n'.join([f'- {b}' for b in platform.get('best_for', [])])
    not_for = '\n'.join([f'- {n}' for n in platform.get('not_ideal_for', [])])

    body = f"""
## Our Verdict

**{name} scores {r['overall']}/10** — {"an excellent choice" if r['overall'] >= 8.5 else "a solid option" if r['overall'] >= 7.5 else "worth considering"} for {cat} in the Feng Shui niche. With a **{a['commission']}% commission rate** and **{a['cookie_days']}-day cookie window**, it's {"a top-tier" if a['commission'] >= 25 else "a decent"} affiliate opportunity.

{platform.get('verdict', '')}

## At a Glance

| Feature | Value |
|:--------|:------|
| Founded | {platform.get('founded', 'N/A')} |
| Headquarters | {platform.get('headquarters', 'N/A')} |
| Languages | {platform.get('language', 'N/A')} |
| Products | {len(platform.get('product_lines', []))} product lines |
| Affiliate | {a.get('network', 'Direct')} |

> *Full rating breakdown, pros & cons, and affiliate details are rendered by the template from `data/fengshui_platforms.yaml`.*

*Last updated: {today}*
""".strip()

    content = fm + body + '\n'

    if not dry_run:
        os.makedirs(page_dir, exist_ok=True)
        with open(page_path, 'w', encoding='utf-8') as f:
            f.write(content)

    return page_path


def generate_comparison(p1, p2, root_dir, today, dry_run=False):
    """Generate a comparison page (flat .md)."""
    if not p1.get('data_complete') or not p2.get('data_complete'):
        return None

    slug = f'{p1["slug"]}-vs-{p2["slug"]}'
    page_path = os.path.join(root_dir, 'vs', f'{slug}.md')

    r1, r2 = p1['ratings']['overall'], p2['ratings']['overall']
    c1, c2 = p1['affiliate']['commission'], p2['affiliate']['commission']
    overall_winner = p1['name'] if r1 >= r2 else p2['name']
    comm_winner = p1['name'] if c1 >= c2 else p2['name']

    q1 = p1['ratings']['product_quality']
    q2 = p2['ratings']['product_quality']
    prod_winner = p1['name'] if q1 >= q2 else p2['name']

    fm = make_frontmatter(
        title=f"{p1['name']} vs {p2['name']}",
        description=f"{p1['name']} ({r1}/10) vs {p2['name']} ({r2}/10) — side-by-side comparison of commissions, products, and ratings.",
        date=str(today),
        type="comparison",
        layout="comparison",
        slug1=p1['slug'],
        slug2=p2['slug'],
        name1=p1['name'],
        name2=p2['name'],
    )

    body = f"""
## Quick Verdict

**Winner: {overall_winner} ({max(r1, r2)}/10)**

| Aspect | {p1['name']} | {p2['name']} | Winner |
|:-------|:------------:|:------------:|:------:|
| Overall | {r1}/10 | {r2}/10 | **{overall_winner}** |
| Commission | {c1}% | {c2}% | **{comm_winner}** |
| Product Quality | {q1}/10 | {q2}/10 | **{prod_winner}** |
| Cookie | {p1['affiliate']['cookie_days']}d | {p2['affiliate']['cookie_days']}d | {"Tie" if p1['affiliate']['cookie_days'] == p2['affiliate']['cookie_days'] else p1['name'] if p1['affiliate']['cookie_days'] > p2['affiliate']['cookie_days'] else p2['name']} |

> Full side-by-side comparison with pros, cons, and affiliate program details is rendered by the template from YAML data.

*Last updated: {today}*
""".strip()

    content = fm + body + '\n'

    if not dry_run:
        with open(page_path, 'w', encoding='utf-8') as f:
            f.write(content)

    return page_path


def generate_best_of(category, platforms, root_dir, today, dry_run=False):
    """Generate a best-of page (flat .md, no type field)."""
    page_path = os.path.join(root_dir, 'best', f'{category}.md')
    cat_title = category.replace('-', ' ').title()

    # Get complete platforms, sorted by rating
    top = sorted(
        [p for p in platforms if p.get('data_complete')],
        key=lambda p: p['ratings']['overall'],
        reverse=True
    )

    desc_map = {
        'products': 'crystals, compasses, cures, and authentic Feng Shui items',
        'courses': 'online courses and certification programs',
        'consulting': 'personalized home and business consultations',
        'books': 'books and learning materials',
        'beginners': 'getting started with Feng Shui',
    }

    cat_desc = desc_map.get(category, 'Feng Shui platforms')

    fm = make_frontmatter(
        title=f"Best {cat_title} Platforms {today.year}",
        description=f"Top Feng Shui platforms for {cat_desc}. Expert rankings with ratings, commissions, and affiliate details.",
        date=str(today),
    )

    rankings = []
    for i, p in enumerate(top[:5]):
        rankings.append(
            f'{i+1}. **[{p["name"]}](/reviews/{p["slug"]}/)** — '
            f'{p["ratings"]["overall"]}/10 '
            f'({p["affiliate"]["commission"]}% commission, {p["affiliate"]["cookie_days"]}d cookie)'
        )
    rankings_text = "\n".join(rankings)

    body = f"""## Best {cat_title} Platforms for {cat_desc.capitalize()}

We ranked {len(top)} platforms on product quality, affiliate commission, support, and reputation.

{rankings_text}

## How We Rank

1. **Product Quality** — authenticity, variety, and quality of products/services
2. **Affiliate Program** — commission rate, cookie duration, payout threshold
3. **Reputation** — years in business, customer reviews, industry standing
4. **Support** — affiliate support, shipping, customer service

> Rankings based on our independent review data. See each platform's full review for details.

*Last updated: {today}*
""".strip()

    content_out = fm + body + '\n'

    if not dry_run:
        with open(page_path, 'w', encoding='utf-8') as f:
            f.write(content_out)

    return page_path


def main():
    parser = argparse.ArgumentParser(description='Generate Hugo pages from YAML')
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--only', choices=['reviews', 'comparisons', 'best'])
    args = parser.parse_args()

    platforms = load_platforms()
    complete = [p for p in platforms if p.get('data_complete')]
    today = date.today()

    print(f'\nMode: {"DRY RUN" if args.dry_run else "WRITE"} | Date: {today}\n')

    review_count = comp_count = best_count = 0

    # --- Reviews ---
    if not args.only or args.only == 'reviews':
        print('=== Reviews ===')
        for p in platforms:
            path = generate_review(p, CONTENT, today, args.dry_run)
            if path:
                review_count += 1
                print(f'  {"📋" if args.dry_run else "✅"} {os.path.relpath(path, BASE)}')
        print(f'  → {review_count} review pages\n')

    # --- Comparisons ---
    if not args.only or args.only == 'comparisons':
        print('=== Comparisons ===')
        for i, p1 in enumerate(complete):
            for j, p2 in enumerate(complete):
                if j <= i:
                    continue
                path = generate_comparison(p1, p2, CONTENT, today, args.dry_run)
                if path:
                    comp_count += 1
                    print(f'  ✅ {os.path.relpath(path, BASE)}')
        expected = len(complete) * (len(complete) - 1) // 2 if len(complete) > 1 else 0
        print(f'  → {comp_count}/{expected} comparison pages\n')

    # --- Best Of ---
    if not args.only or args.only == 'best':
        print('=== Best Of ===')
        for cat in ['products', 'courses', 'consulting', 'books', 'beginners']:
            path = generate_best_of(cat, complete, CONTENT, today, args.dry_run)
            if path:
                best_count += 1
                print(f'  ✅ {os.path.relpath(path, BASE)}')
        print(f'  → {best_count} best-of pages\n')

    # --- Summary ---
    total = review_count + comp_count + best_count
    print('=' * 55)
    print(f'Total: {total} pages ({review_count} reviews + {comp_count} comparisons + {best_count} best-of)')
    if args.dry_run:
        print('Dry run — add --dry-run to preview, remove to write files.')
    else:
        print('Done! Run: hugo server -D')
        print('Then:  python scripts/quality_check.py')
    print('=' * 55)


if __name__ == '__main__':
    main()
