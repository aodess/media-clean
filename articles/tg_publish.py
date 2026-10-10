import json,sys,os,urllib.request,urllib.parse,re
API='https://api.telegra.ph/'
def call(m, **kw):
    return json.load(urllib.request.urlopen(urllib.request.Request(API+m, data=urllib.parse.urlencode(kw).encode()), timeout=30))
def inline(t):
    out=[];pos=0
    for m in re.finditer(r'\[([^\]]+)\]\(([^)]+)\)',t):
        if m.start()>pos: out.append(t[pos:m.start()])
        out.append({'tag':'a','attrs':{'href':m.group(2)},'children':[m.group(1)]}); pos=m.end()
    if pos<len(t): out.append(t[pos:])
    return out
def nodes(md):
    res=[];ul=None;ol=None
    for line in md.strip().splitlines():
        if line.startswith('- '):
            if ul is None: ul={'tag':'ul','children':[]}; res.append(ul)
            ul['children'].append({'tag':'li','children':inline(line[2:])}); continue
        ul=None
        if line.startswith('## '): res.append({'tag':'h3','children':[line[3:]]})
        elif line.strip(): res.append({'tag':'p','children':inline(line)})
    return res
TOKF='/data/telegraph_mediaclean_token.txt'
if os.path.exists(TOKF): tok=open(TOKF).read().strip()
else:
    tok=call('createAccount', short_name='MediaClean', author_name='Media Clean', author_url='https://t.me/AIMediaclean_bot')['result']['access_token']
    open(TOKF,'w').write(tok); os.chmod(TOKF,0o600)
f,title=sys.argv[1],sys.argv[2]
r=call('createPage', access_token=tok, title=title, author_name='Media Clean', author_url='https://t.me/AIMediaclean_bot', content=json.dumps(nodes(open(f).read()),ensure_ascii=False), return_content='false')
print(r['result']['url'] if r.get('ok') else r)
