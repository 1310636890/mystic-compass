# Mystic Compass

**Feng Shui & Chinese Metaphysics PSEO Affiliate Site**

> Your compass for navigating the world of Feng Shui platforms — reviews, comparisons, and guides.

---

## What This Is

A Hugo static site that programmatically generates:
- **12 platform reviews** (detail pages with ratings, pricing, pros/cons)
- **66 comparison pages** (NxN: every platform compared to every other)
- **5 Best Of guides** (curated rankings by category)
- **10+ educational guides** (SEO-optimized Feng Shui content)

## How It Works

```
data/fengshui_platforms.yaml   ← Single source of truth (12 platforms)
        ↓
scripts/generate_pages.py      ← Reads YAML → generates Hugo .md files
        ↓
content/reviews/*.md           ← Auto-generated review pages
content/vs/*-vs-*.md           ← Auto-generated comparison pages
        ↓
hugo build                     ← Hugo builds static HTML
        ↓
public/                        ← Ready to deploy to GitHub Pages / Cloudflare
```

## Quick Start

### 1. Prerequisites

```bash
# Install Hugo (extended version)
# Windows: choco install hugo-extended
# Mac:     brew install hugo
# Linux:   snap install hugo

# Install Python deps
pip install pyyaml
```

### 2. Generate Pages

```bash
cd C:/Users/rjw/Desktop/mystic-compass
python scripts/generate_pages.py
```

### 3. Preview Locally

```bash
hugo server -D
# Open http://localhost:1313
```

### 4. Quality Check

```bash
python scripts/quality_check.py
# python scripts/quality_check.py --level 2  # Content-only check
```

### 5. Build for Production

```bash
hugo --minify
# Output: public/
```

---

## Deployment (NO SERVER NEEDED)

### Option A: GitHub Pages (Free)

```
1. Create GitHub repo: mystic-compass
2. Push code:
   git init
   git add .
   git commit -m "Init Mystic Compass"
   git remote add origin https://github.com/YOUR_USER/mystic-compass.git
   git push -u origin main

3. Enable GitHub Actions in repo Settings → Actions → Allow
4. Push again → GitHub Actions auto-builds Hugo → deploys to gh-pages branch
5. Go to Settings → Pages → Source: "Deploy from a branch" → gh-pages → Save
6. Your site is live at: https://YOUR_USER.github.io/mystic-compass/
```

**Deploy happens automatically on every `git push`.**

### Option B: Cloudflare Pages (Free + Faster CDN)

```
1. Push code to GitHub (same as above)
2. Go to Cloudflare Dashboard → Pages → Create a project
3. Connect your GitHub repo
4. Build settings:
   - Framework preset: Hugo
   - Build command: hugo --minify
   - Build output directory: public
5. Deploy
6. Add your custom domain (mystic-compass.com) in Cloudflare Pages settings
```

**Both options: $0/month, no server to manage, automatic HTTPS.**

---

## Adding Your Domain

```
1. Buy mystic-compass.com (Namecheap ~$11/year)
2. In Cloudflare Pages → Custom Domains → Add mystic-compass.com
3. Update domain DNS to point to Cloudflare nameservers
4. Wait for DNS propagation (5-30 min)
```

---

## Project Structure

```
mystic-compass/
├── archetypes/              # Hugo archetypes (page templates)
├── content/
│   ├── _index.md            # Homepage content
│   ├── reviews/             # 12 platform review pages (auto-generated)
│   ├── vs/                  # 66 comparison pages (auto-generated)
│   ├── best/                # 5 best-of pages (semi-generated)
│   ├── guide/               # 10+ educational guides (hand-written)
│   └── east-west/           # East-West bridge content
├── data/
│   └── fengshui_platforms.yaml  # 12 platforms — THE source of truth
├── layouts/
│   ├── _default/
│   │   ├── baseof.html      # Base HTML template
│   │   ├── single.html      # Guide page template
│   │   └── list.html        # Section listing template
│   ├── index.html           # Homepage template
│   ├── review/
│   │   └── single.html      # Review page template
│   ├── comparison/
│   │   └── single.html      # Comparison page template
│   └── partials/            # Reusable components
├── scripts/
│   ├── generate_pages.py    # YAML → Hugo .md generator
│   └── quality_check.py     # L0-L3 quality checker
├── static/
│   ├── css/style.css        # Site stylesheet
│   └── images/              # Platform logos & images
├── .github/workflows/
│   └── hugo-deploy.yml      # Auto-deploy to GitHub Pages
├── config.yaml              # Hugo configuration
├── .gitignore
└── README.md
```

---

## Adding Content

### Add a new platform to data/fengshui_platforms.yaml

```yaml
  - id: new-platform
    name: New Platform
    slug: new-platform
    url: https://...
    category: products
    priority: 2
    has_affiliate: true
    affiliate:
      commission: 15
      commission_type: percentage
      cookie_days: 30
      network: direct
      auto_approve: true
    # ... fill in ratings, pros, cons, etc.
```

Then re-run: `python scripts/generate_pages.py`

### Write a new guide

```bash
hugo new guide/what-is-feng-shui.md
# Edit content/guide/what-is-feng-shui.md
```

---

## SEO Checklist

- [x] robots.txt (auto-generated by Hugo)
- [x] Sitemap (auto-generated: /sitemap.xml)
- [x] Canonical URLs (set in baseof.html)
- [x] Meta descriptions (every page)
- [x] Semantic HTML (H1 → H2 → H3 hierarchy)
- [x] Breadcrumb navigation (review & comparison pages)
- [x] Affiliate disclosure (every monetized page)
- [x] Mobile responsive (CSS grid, no fixed widths)
- [x] Fast loading (static HTML, no JS framework)
- [ ] Google Analytics (add GA4 ID to config.yaml)
- [ ] Google Search Console (verify domain after launch)

---

## Platform Data Status

| # | Platform | Data Filled | Affiliate Applied |
|---|----------|:-----------:|:-----------------:|
| 1 | Feng Shui World | ✅ Complete | ⬜ Pending |
| 2 | Feng Shui Online | ✅ Complete | ⬜ Pending |
| 3 | Joey Yap | ✅ Complete | ⬜ Pending |
| 4-12 | Remaining 9 platforms | ⬜ Minimal | ⬜ Pending |

> **Action**: Fill in platforms 4-12 data on Day 3-6 after researching each platform's affiliate program.

---

## Tech Stack

- **Static Site**: Hugo (Go, ultra-fast builds)
- **Data**: YAML (human-readable, git-diffable)
- **Styling**: Vanilla CSS (no framework, minimal)
- **Hosting**: GitHub Pages or Cloudflare Pages ($0)
- **CI/CD**: GitHub Actions (auto-deploy on push)

**Total monthly cost: $0** (plus ~$11/year for domain)

<!-- auto-deploy verified -->
