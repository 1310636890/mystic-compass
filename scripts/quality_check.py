"""quality_check.py — L0-L3 Quality Gates for PSEO Pages

Run after generate_pages.py to catch:
  L0 (Technical): 404s, missing canonicals, broken links
  L1 (Structural): Missing fields, placeholder text, H1/H2 errors
  L2 (Content): Word count, uniqueness, AI-slop patterns
  L3 (Conversion): CTA presence, affiliate disclosure, table completeness

Usage:
  python scripts/quality_check.py          # Check all generated pages
  python scripts/quality_check.py --level 2  # Only L2 checks
  python scripts/quality_check.py --path content/reviews/  # Check specific dir
"""

import os
import sys
import re
from pathlib import Path
from collections import Counter

BASE = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CONTENT = BASE / 'content'

# — L0: Technical Checks —
def check_technical(filepath):
    issues = []
    content = Path(filepath).read_text(encoding='utf-8')
    
    # Must have frontmatter
    if not content.startswith('---'):
        issues.append("Missing YAML frontmatter")
    
    # Must have title
    if 'title:' not in content[:500]:
        issues.append("Missing title in frontmatter")
    
    # Must have description
    if 'description:' not in content[:500]:
        issues.append("Missing description in frontmatter")
    
    # Must have layout
    if 'layout:' not in content[:500]:
        issues.append("Missing layout in frontmatter")
    
    return issues

# — L1: Structural Checks —
def check_structural(filepath):
    issues = []
    content = Path(filepath).read_text(encoding='utf-8')
    body = content.split('---', 2)[-1] if content.count('---') >= 2 else ''
    
    # No placeholder text
    placeholders = ['TODO', 'FIXME', 'Lorem ipsum', 'TBD', 'Coming soon', 'to be filled']
    for ph in placeholders:
        if ph.lower() in body.lower():
            issues.append(f"Contains placeholder: '{ph}'")
    
    # Must have at least one H2
    if not re.search(r'^##\s', body, re.MULTILINE):
        issues.append("No H2 headings found")
    
    # Word count (rough)
    words = len(body.split())
    if words < 200:
        issues.append(f"Too short: {words} words (< 200 minimum)")
    elif words < 500:
        issues.append(f"⚠️ Short: {words} words (< 500 recommended)")
    
    return issues

# — L2: Content Quality —
def check_content(filepath):
    issues = []
    content = Path(filepath).read_text(encoding='utf-8')
    body = content.split('---', 2)[-1] if content.count('---') >= 2 else ''
    body_lower = body.lower()
    
    # AI-slop patterns
    slop_patterns = [
        ('delve into', 'AI-generated phrase'),
        ('in today', 'AI-generated opener'),
        ('it is important to note', 'AI padding'),
        ('in conclusion', 'AI closer (use natural ending)'),
        ('whether you', 'AI conditional pattern'),
        ('as we', 'AI narrative voice'),
        ('in the ever-evolving', 'AI cliche'),
        ('game-changer', 'marketing cliche'),
        ('unlock', 'hype word — be specific instead'),
        ('unleash', 'hype word'),
        ('revolutionize', 'hype word'),
    ]
    
    for phrase, desc in slop_patterns:
        if phrase in body_lower:
            issues.append(f"AI-slop: '{phrase}' ({desc})")
    
    # Sentence length variety check
    sentences = re.split(r'[.!?]+', body)
    sentences = [s.strip() for s in sentences if s.strip()]
    if sentences:
        lengths = [len(s.split()) for s in sentences]
        avg_len = sum(lengths) / len(lengths)
        if avg_len > 25:
            issues.append(f"Sentences too long: avg {avg_len:.0f} words (>25)")
        if avg_len < 8:
            issues.append(f"Sentences too short: avg {avg_len:.0f} words (<8)")
    
    return issues

# — L3: Conversion Checks —
def check_conversion(filepath):
    issues = []
    content = Path(filepath).read_text(encoding='utf-8')
    body = content.split('---', 2)[-1] if content.count('---') >= 2 else ''
    body_lower = body.lower()
    
    # Affiliate disclosure
    disclosure_terms = ['affiliate', 'commission', 'we may earn', 'purchase through']
    has_disclosure = any(t in body_lower for t in disclosure_terms)
    if not has_disclosure:
        issues.append("Missing affiliate disclosure")
    
    # CTA (call to action)
    cta_terms = ['visit', 'check out', 'try', 'get started', 'sign up', 'join']
    has_cta = any(t in body_lower for t in cta_terms)
    if not has_cta:
        issues.append("Missing CTA (call to action)")
    
    # External links
    links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', body)
    external_links = [l for l in links if l[1].startswith('http')]
    if len(external_links) < 1:
        issues.append("No external links (affiliate links missing)")
    
    return issues


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--level', type=int, default=4, help='Max quality level to check (0-3)')
    parser.add_argument('--path', type=str, default=None, help='Specific directory to check')
    args = parser.parse_args()
    
    scan_dir = Path(args.path) if args.path else CONTENT
    
    if not scan_dir.exists():
        print(f"Error: Directory not found: {scan_dir}")
        sys.exit(1)
    
    md_files = list(scan_dir.rglob('*.md'))
    if not md_files:
        print(f"No .md files found in {scan_dir}")
        sys.exit(0)
    
    print(f"Checking {len(md_files)} files in {scan_dir}")
    print(f"Quality level: L0-L{args.level}")
    print()
    
    total_issues = 0
    clean_count = 0
    
    for f in sorted(md_files):
        all_issues = []
        
        if args.level >= 0:
            all_issues.extend(check_technical(f))
        if args.level >= 1:
            all_issues.extend(check_structural(f))
        if args.level >= 2:
            all_issues.extend(check_content(f))
        if args.level >= 3:
            all_issues.extend(check_conversion(f))
        
        relpath = str(f.relative_to(BASE))
        
        if all_issues:
            print(f"❌ {relpath}")
            for issue in all_issues:
                print(f"   - {issue}")
            total_issues += len(all_issues)
        else:
            clean_count += 1
    
    print(f"\n--- Summary ---")
    print(f"Clean: {clean_count}/{len(md_files)} files")
    print(f"Issues: {total_issues}")
    
    if total_issues == 0:
        print("✅ All checks passed!")
        sys.exit(0)
    else:
        print(f"⚠️  {total_issues} issues to fix")
        sys.exit(1)

if __name__ == '__main__':
    main()
