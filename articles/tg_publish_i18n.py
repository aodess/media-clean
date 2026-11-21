"""Publish i18n/<code>.json articles to telegra.ph.
Usage: python3 tg_publish_i18n.py zh ar            (every article of each pack)
       python3 tg_publish_i18n.py --slug <slug> es (only that article; daily additions, no duplicates)"""
import json, re, sys, urllib.parse, urllib.request
API = 'https://api.telegra.ph/'
TOKEN = open('/data/telegraph_mediaclean_token.txt').read().strip()

def call(m, **kw):
    data = urllib.parse.urlencode(kw).encode()
    return json.load(urllib.request.urlopen(urllib.request.Request(API + m, data=data), timeout=30))

def inline(t):
    out, pos = [], 0
    for m in re.finditer(r'\[([^\]]+)\]\(([^)]+)\)', t):
        if m.start() > pos: out.append(t[pos:m.start()])
        out.append({'tag': 'a', 'attrs': {'href': m.group(2)}, 'children': [m.group(1)]}); pos = m.end()
    if pos < len(t): out.append(t[pos:])
    return out

def nodes(md):
    res, ul = [], None
    for line in md.split('\n'):
        if line.startswith('- '):
            if ul is None: ul = {'tag': 'ul', 'children': []}; res.append(ul)
            ul['children'].append({'tag': 'li', 'children': inline(line[2:])}); continue
        ul = None
        if line.startswith('## '): res.append({'tag': 'h3', 'children': [line[3:]]})
        elif line.strip(): res.append({'tag': 'p', 'children': inline(line)})
    return res

args = sys.argv[1:]
only = None
if '--slug' in args:
    i = args.index('--slug'); only = args[i + 1]; del args[i:i + 2]
for code in args:
    import os
    p = f'i18n/{code}.json' if os.path.exists(f'i18n/{code}.json') else f'i18n/{code}_articles.json' if os.path.exists(f'i18n/{code}_articles.json') else f'i18n/{code}.json'
    d = json.load(open(p))
    for a in d['articles']:
        if only and a['slug'] != only:
            continue
        r = call('createPage', access_token=TOKEN, title=a['title'][:256], author_name='Media Clean',
                 author_url='https://t.me/AIMediaclean_bot', content=json.dumps(nodes(a['body']), ensure_ascii=False))
        print(code, r['result']['url'] if r.get('ok') else r)
