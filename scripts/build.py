"""Build a small Markdown blog. Run from any directory: python3 scripts/build.py."""
from pathlib import Path
import datetime as dt
import html
import json
import re
import shutil
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'docs'
BASE = 'https://zhang-hl-1.github.io'


def build():
    if OUT.exists():
        shutil.rmtree(OUT)
    shutil.copytree(ROOT / 'site', OUT)
    (OUT / '.nojekyll').touch()
    posts = []
    for source in sorted((ROOT / 'content/posts').glob('*.md')):
        if not re.fullmatch(r'[a-z0-9][a-z0-9-]*', source.stem):
            raise ValueError(f'Use a lowercase English slug: {source.name}')
        raw = source.read_text(encoding='utf-8')
        parts = raw.split('---', 2)
        if len(parts) != 3 or parts[0].strip():
            raise ValueError(f'Missing metadata: {source.name}')
        meta = dict(line.split(':', 1) for line in parts[1].strip().splitlines() if ':' in line)
        meta = {k.strip(): v.strip() for k, v in meta.items()}
        for key in ('title', 'date', 'category', 'description'):
            if not meta.get(key):
                raise ValueError(f'Missing {key}: {source.name}')
        dt.date.fromisoformat(meta['date'])
        if meta.get('draft', '').lower() == 'true':
            continue
        import markdown
        body = markdown.markdown(parts[2], extensions=['fenced_code', 'tables', 'toc', 'sane_lists'])
        title, date, category, description = (html.escape(meta[k], quote=True) for k in ('title', 'date', 'category', 'description'))
        url = f'/posts/{source.stem}/'
        page = f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title} · 小鳥遊</title><meta name="description" content="{description}"><link rel="canonical" href="{BASE}{url}"><link rel="stylesheet" href="/style.css"><link rel="icon" href="/favicon.svg"><link rel="alternate" type="application/rss+xml" href="/rss.xml" title="RSS"><script>try{{document.documentElement.dataset.theme=localStorage.getItem('theme')||(matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light')}}catch(e){{}}</script><script src="/app.js" defer></script></head><body><a class="skip" href="#main">跳到正文</a><header class="header wrap"><a class="brand" href="/">小鳥遊 / JOURNAL</a><nav><a href="/#journal">所有文章</a><button id="theme" class="theme" aria-label="切换深浅色主题">◐</button></nav></header><main id="main" class="wrap reading"><p class="eyebrow">{category} · <time datetime="{date}">{date}</time></p><h1>{title}</h1><p class="intro">{description}</p><article class="prose">{body}</article><p style="margin-top:60px"><a class="text-link" href="/#journal">← 返回文章列表</a></p></main><footer class="footer wrap"><span>© <span id="year">2026</span> 小鳥遊</span><a href="/rss.xml">RSS ↗</a></footer></body></html>'''
        destination = OUT / url.strip('/') / 'index.html'
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(page, encoding='utf-8')
        posts.append({**{k: meta[k] for k in ('title', 'date', 'category', 'description')}, 'url': url, 'text': re.sub('<[^>]+>', ' ', body), 'body': body})
    posts.sort(key=lambda p: (p['date'], p['url']), reverse=True)
    (OUT / 'posts.json').write_text(json.dumps([{k: v for k, v in p.items() if k != 'body'} for p in posts], ensure_ascii=False, indent=2), encoding='utf-8')
    rss = ET.Element('rss', version='2.0')
    channel = ET.SubElement(rss, 'channel')
    for key, value in [('title', '小鳥遊'), ('link', BASE + '/'), ('description', '技术、学习与日常的记录'), ('language', 'zh-CN')]:
        ET.SubElement(channel, key).text = value
    for p in posts:
        item = ET.SubElement(channel, 'item')
        for key, value in [('title', p['title']), ('link', BASE + p['url']), ('guid', BASE + p['url']), ('description', p['body']), ('pubDate', dt.datetime.strptime(p['date'], '%Y-%m-%d').strftime('%a, %d %b %Y 00:00:00 +0800'))]:
            ET.SubElement(item, key).text = value
    ET.ElementTree(rss).write(OUT / 'rss.xml', encoding='utf-8', xml_declaration=True)
    sitemap = ET.Element('urlset', xmlns='http://www.sitemaps.org/schemas/sitemap/0.9')
    for path in ['/'] + [p['url'] for p in posts]:
        ET.SubElement(ET.SubElement(sitemap, 'url'), 'loc').text = BASE + path
    ET.ElementTree(sitemap).write(OUT / 'sitemap.xml', encoding='utf-8', xml_declaration=True)
    (OUT / 'robots.txt').write_text(f'User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n')
    (OUT / '404.html').write_text('''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>未找到页面 · 小鳥遊</title><link rel="stylesheet" href="/style.css"><main class="wrap reading"><p class="eyebrow">404 / NOT FOUND</p><h1>这页笔记不在这里。</h1><p>博客已经重新搭建，旧文章链接可能已经失效。</p><a class="text-link" href="/">返回首页 →</a></main></html>''', encoding='utf-8')
    print(f'Built {len(posts)} posts into {OUT}')


if __name__ == '__main__':
    build()
