"""Builds zh/ar landing pages and articles from i18n/*.json. Run: python3 build_i18n.py"""
import html, json, re
CSS = open('public/index.html').read().split('<style>')[1].split('</style>')[0]
RTL = "body{direction:rtl;text-align:right}nav{flex-direction:row-reverse}"
ALT = ('<link rel="alternate" hreflang="en" href="__SITE__/">\n<link rel="alternate" hreflang="ru" href="__SITE__/ru/">\n'
       '<link rel="alternate" hreflang="zh-Hans" href="__SITE__/zh/">\n<link rel="alternate" hreflang="ar" href="__SITE__/ar/">\n'
       '<link rel="alternate" hreflang="x-default" href="__SITE__/">')
LINKS = '<a href="/">English</a> · <a href="/ru/">Русский</a> · <a href="/zh/">中文</a> · <a href="/ar/">العربية</a>'
e = lambda s: html.escape(s, quote=True)

def inline(t):
    t = html.escape(t, quote=False)
    return re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2" style="color:var(--accent)">\1</a>', t)

def body(md):
    out, ul = [], False
    for l in md.split('\n'):
        if l.startswith('- '):
            if not ul: out.append('<ul>'); ul = True
            out.append('<li>' + inline(l[2:]) + '</li>'); continue
        if ul: out.append('</ul>'); ul = False
        if l.startswith('## '): out.append('<h2>' + e(l[3:]) + '</h2>')
        elif l.strip(): out.append('<p>' + inline(l) + '</p>')
    if ul: out.append('</ul>')
    return '\n'.join(out)

def head(d, title, desc, canon, extra_ld, alternates=True):
    return f'''<!doctype html>
<html lang="{d['lang']}" dir="{d['dir']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="__SITE__{canon}">
{ALT if alternates else ''}
<meta property="og:type" content="website"><meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}"><meta property="og:url" content="__SITE__{canon}">
<meta property="og:image" content="__SITE__/og.png"><meta property="og:locale" content="{d['lang'].replace('-', '_')}">
<meta name="twitter:card" content="summary_large_image"><meta name="theme-color" content="#06122b">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<script type="application/ld+json">{json.dumps(extra_ld, ensure_ascii=False)}</script>
<style>{CSS}{RTL if d['dir'] == 'rtl' else ''}article p,article li{{color:#cfdcf5}}article h2{{font-size:24px}}article{{max-width:720px}}</style>
</head>'''

def landing(d):
    p, bot = d['path'], 'https://t.me/AIMediaclean_bot?start=' + d['start']
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "SoftwareApplication", "name": "Media Clean", "applicationCategory": "MultimediaApplication",
         "operatingSystem": "Telegram", "url": "https://t.me/AIMediaclean_bot", "inLanguage": d['lang'],
         "description": d['desc'], "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}},
        {"@type": "FAQPage", "inLanguage": d['lang'], "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in d['qa']]}]}
    cards = lambda items: '\n'.join(f'<div class="card"><b>{e(a)}</b>{e(b)}</div>' for a, b in items)
    faq = '\n'.join(f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in d['qa'])
    arts = '\n'.join(f'<li><a href="/blog/{a["slug"]}" style="color:var(--accent)">{e(a["title"])}</a></li>' for a in d['articles'])
    return head(d, d['title'], d['desc'], f'/{p}/', ld) + f'''
<body>
<div class="wrap">
<nav><span>✨ Media Clean</span><span>{LINKS}</span></nav>
<h1>{e(d['h1'])}</h1>
<p class="lead">{e(d['lead'])}</p>
<a class="btn" href="{bot}">{e(d['btn'])}</a>
<h2>{e(d['how'])}</h2>
<div class="grid">
{cards(d['steps'])}
</div>
<h2>{e(d['get'])}</h2>
<div class="grid">
{cards(d['cards'])}
</div>
<h2>{e(d['faq'])}</h2>
{faq}
<h2>{e(d['nav_blog'])}</h2>
<ul>{arts}</ul>
<p style="margin-top:36px"><a class="btn" href="{bot}">{e(d['btn2'])}</a></p>
<footer>© Media Clean · <a href="https://t.me/AIMediaclean_bot">@AIMediaclean_bot</a> · {LINKS}</footer>
</div>
</body>
</html>
'''

def article(d, a):
    ld = {"@context": "https://schema.org", "@type": "Article", "headline": a['title'], "inLanguage": d['lang'],
          "author": {"@type": "Organization", "name": "Media Clean"}, "datePublished": "2026-11-09",
          "mainEntityOfPage": "__SITE__/blog/" + a['slug']}
    bot = 'https://t.me/AIMediaclean_bot?start=blog_' + d['path']
    return head(d, a['title'] + ' — Media Clean', a['desc'], '/blog/' + a['slug'], ld, alternates=False) + f'''
<body><div class="wrap"><nav><a href="/{d['path']}/">✨ Media Clean</a></nav>
<article><h1 style="font-size:clamp(26px,5vw,40px)">{e(a['title'])}</h1>
{body(a['body'])}
<p style="margin-top:32px"><a class="btn" href="{bot}">{e(d['btn'])}</a></p></article>
<footer><a href="/{d['path']}/">Media Clean</a> · <a href="https://t.me/AIMediaclean_bot">@AIMediaclean_bot</a></footer></div></body></html>
'''

urls = []
for code in ('zh', 'ar'):
    d = json.load(open(f'i18n/{code}.json'))
    import os; os.makedirs(f'public/{code}', exist_ok=True)
    open(f'public/{code}/index.html', 'w').write(landing(d))
    urls.append(f'/{code}/')
    for a in d['articles']:
        open(f'public/blog/{a["slug"]}.html', 'w').write(article(d, a))
        urls.append('/blog/' + a['slug'])

# hreflang on the EN/RU landings
for f in ('public/index.html', 'public/ru/index.html'):
    s = open(f).read()
    s = re.sub(r'(<link rel="alternate" hreflang="[^"]+" href="[^"]+">\n?)+', ALT + '\n', s, count=1)
    open(f, 'w').write(s)

# sitemap: one entry per page, landing alternates
alts = ''.join(f'<xhtml:link rel="alternate" hreflang="{h}" href="__SITE__{u}"/>' for h, u in
               (('en', '/'), ('ru', '/ru/'), ('zh-Hans', '/zh/'), ('ar', '/ar/')))
s = open('public/sitemap.xml').read()
for u in ('/', '/ru/', '/zh/', '/ar/'):
    s = re.sub(r'<url><loc>__SITE__' + re.escape(u) + r'</loc>.*?</url>\n?', '', s)
land = ''.join(f'<url><loc>__SITE__{u}</loc>{alts}</url>\n' for u in ('/', '/ru/', '/zh/', '/ar/'))
s = s.replace('xmlns:xhtml="http://www.w3.org/1999/xhtml">\n', 'xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + land, 1)
for u in urls:
    if u.startswith('/blog/') and f'__SITE__{u}<' not in s:
        s = s.replace('</urlset>', f'<url><loc>__SITE__{u}</loc></url>\n</urlset>')
open('public/sitemap.xml', 'w').write(s)
print('built', urls)
