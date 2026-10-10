import re,html,json,os
arts=[
 ("a1.md","what-are-metadata-in-ai-files","Что такое метаданные в ИИ-картинках и видео и откуда они берутся","Какие служебные записи хранят фото и видео из нейросетей: EXIF, XMP, IPTC, C2PA, и что чистка метаданных не делает."),
 ("a2.md","checklist-before-posting-ai-media","Чеклист перед публикацией ИИ-видео и фото: что проверить","Короткий список перед загрузкой в соцсети: отметка ИИ, проверка файла, очистка метаданных."),
 ("a3.md","false-ai-label-on-real-photo","Instagram поставил «Сделано с помощью ИИ» на настоящее фото: почему и что делать","Почему соцсети ставят метку ИИ на обычные фото и как действовать, если это ошибка."),
 ("a4.md","remove-geolocation-from-photo","Как удалить геолокацию из фото перед отправкой: iPhone, Android, Windows","Как выключить запись геопозиции в камере и убрать координаты из готового фото."),
 ("a6.md","how-to-view-photo-video-metadata","Как посмотреть метаданные фото и видео: Windows, Mac, iPhone, Android","Как открыть служебные данные файла на компьютере и телефоне и что в них искать."),
 ("a7.md","what-is-c2pa-content-credentials","Что такое C2PA и Content Credentials простыми словами","Что хранит подписанная запись о происхождении файла, как её проверить и чего она не гарантирует."),
 ("a5.md","remove-video-metadata","Метаданные видео: что внутри mp4 и как их убрать","Что хранится в видеофайле и четыре способа его очистить, включая перекодирование."),
]
CSS=open('public/index.html').read().split('<style>')[1].split('</style>')[0]
def inline(t):
    t=html.escape(t,quote=False)
    return re.sub(r'\[([^\]]+)\]\(([^)]+)\)',r'<a href="\2" style="color:var(--accent)">\1</a>',t)
def body(md):
    out=[];ul=False
    for l in md.strip().splitlines():
        if l.startswith('- '):
            if not ul: out.append('<ul>');ul=True
            out.append('<li>'+inline(l[2:])+'</li>');continue
        if ul: out.append('</ul>');ul=False
        if l.startswith('## '): out.append('<h2>'+html.escape(l[3:])+'</h2>')
        elif l.strip(): out.append('<p>'+inline(l)+'</p>')
    if ul: out.append('</ul>')
    return '\n'.join(out)
os.makedirs('public/blog',exist_ok=True)
extra="article p,article li{color:#cfdcf5}article h2{font-size:24px}article{max-width:720px}"
for f,slug,title,desc in arts:
    b=body(open('articles/'+f).read())
    ld=json.dumps({"@context":"https://schema.org","@type":"Article","headline":title,"inLanguage":"ru","author":{"@type":"Organization","name":"Media Clean"},"mainEntityOfPage":"__SITE__/blog/%s"%slug,"datePublished":"2026-10-10"},ensure_ascii=False)
    page=f'''<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)} — Media Clean</title><meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="__SITE__/blog/{slug}"><meta property="og:type" content="article"><meta property="og:title" content="{html.escape(title)}"><meta property="og:description" content="{html.escape(desc)}"><meta property="og:image" content="__SITE__/og.png"><meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.svg" type="image/svg+xml"><script type="application/ld+json">{ld}</script><style>{CSS}{extra}</style></head>
<body><div class="wrap"><nav><a href="/ru/">✨ Media Clean</a><a href="/blog/">Блог</a></nav>
<article><h1 style="font-size:clamp(26px,5vw,40px)">{html.escape(title)}</h1>
{b}
<p style="margin-top:32px"><a class="btn" href="https://t.me/AIMediaclean_bot?start=blog">Открыть бота в Telegram →</a></p></article>
<footer><a href="/blog/">Все статьи</a> · <a href="/ru/">Media Clean</a> · <a href="https://t.me/AIMediaclean_bot">@AIMediaclean_bot</a></footer></div></body></html>'''
    open(f'public/blog/{slug}.html','w').write(page)
lis=''.join(f'<div class="card" style="margin-bottom:12px"><b><a href="/blog/{s}" style="color:var(--accent);text-decoration:none">{html.escape(t)}</a></b>{html.escape(d)}</div>' for f,s,t,d in arts)
idx=f'''<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Блог Media Clean — метаданные фото и видео</title><meta name="description" content="Статьи о метаданных фото и видео: геолокация, EXIF, метки ИИ, очистка файлов.">
<link rel="canonical" href="__SITE__/blog/"><link rel="icon" href="/favicon.svg" type="image/svg+xml"><meta property="og:image" content="__SITE__/og.png"><style>{CSS}</style></head>
<body><div class="wrap"><nav><a href="/ru/">✨ Media Clean</a><a href="/">English</a></nav><h1>Блог</h1>{lis}
<footer><a href="https://t.me/AIMediaclean_bot?start=blog">@AIMediaclean_bot</a></footer></div></body></html>'''
open('public/blog/index.html','w').write(idx)
sm=open('public/sitemap.xml').read()
sm=re.sub(r'<url><loc>__SITE__/blog.*?</url>\n?','',sm,flags=re.S)
add='<url><loc>__SITE__/blog/</loc></url>\n'+''.join(f'<url><loc>__SITE__/blog/{s}</loc></url>\n' for _,s,_,_ in arts)
sm=sm.replace('</urlset>',add+'</urlset>')
open('public/sitemap.xml','w').write(sm)
