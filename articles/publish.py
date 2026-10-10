import re, json, sys, urllib.request, urllib.parse
API='https://api.telegra.ph/'
def call(m, **kw):
    data=urllib.parse.urlencode(kw).encode()
    return json.load(urllib.request.urlopen(urllib.request.Request(API+m, data=data), timeout=30))
def inline(t):
    out=[];pos=0
    for m in re.finditer(r'\[([^\]]+)\]\(([^)]+)\)',t):
        if m.start()>pos: out.append(t[pos:m.start()])
        out.append({'tag':'a','attrs':{'href':m.group(2)},'children':[m.group(1)]}); pos=m.end()
    if pos<len(t): out.append(t[pos:])
    return out
def nodes(md):
    res=[];ul=None
    for line in md.strip().splitlines():
        if line.startswith('- '):
            if ul is None: ul={'tag':'ul','children':[]}; res.append(ul)
            ul['children'].append({'tag':'li','children':inline(line[2:])}); continue
        ul=None
        if line.startswith('## '): res.append({'tag':'h3','children':[line[3:]]})
        elif line.strip(): res.append({'tag':'p','children':inline(line)})
    return res
acc=call('createAccount', short_name='MediaClean', author_name='Media Clean', author_url='https://t.me/AIMediaclean_bot')['result']
tok=acc['access_token']
pages=[('a1.md','Что такое метаданные в ИИ-картинках и видео и откуда они берутся'),('a2.md','Чеклист перед публикацией ИИ-видео и фото: что проверить')]
for f,title in pages:
    r=call('createPage', access_token=tok, title=title, author_name='Media Clean', author_url='https://t.me/AIMediaclean_bot', content=json.dumps(nodes(open(f).read()),ensure_ascii=False), return_content='false')
    print(r['result']['url'] if r.get('ok') else r)
