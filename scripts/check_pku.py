import urllib.request, re, ssl
ctx = ssl.create_default_context()
req = urllib.request.Request('https://www.pku.edu.cn/', headers={'User-Agent':'Mozilla/5.0'})
html = urllib.request.urlopen(req, timeout=15, context=ctx).read().decode('utf-8','ignore')
srcs = re.findall(r'<img[^>]*src=["\']([^"\']+)["\'][^>]*>', html, re.I)
print('\n'.join(srcs[:20]))
print('---logos---')
for m in re.finditer(r'<img[^>]*>', html, re.I):
    tag = m.group(0)
    if re.search(r'logo|校徽|标识|pku|北大', tag, re.I):
        print(tag[:200])
