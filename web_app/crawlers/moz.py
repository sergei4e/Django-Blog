import sys
import os
import django
import pdb
import requests
from io import BytesIO
from PIL import Image
from lxml import html
import dateutil.parser
from utils.gtrans import translate_text, translate_html
from bs4 import BeautifulSoup
from slugify import slugify


P = os.path.abspath(__file__)
P = os.path.dirname(P)
P = os.path.dirname(P)
sys.path.append(P)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "seoshnik.settings")
django.setup()

from blog.models import Article, Category

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:50.0) Gecko/20100101 Firefox/50.0'}

main_url = 'https://moz.com/blog'
resp = requests.get(main_url, headers=headers)
urls = html.fromstring(resp.text).xpath('//h2/a/@href')
images = html.fromstring(resp.text).xpath('//article//img[@class="post-image"]/@src')

for i in range(2, 21, 1):
    url = f'{main_url}?page={i}'
    resp = requests.get(f'{main_url}?page={i}', headers=headers)
    urls += html.fromstring(resp.text).xpath('//h2/a/@href')
    images += html.fromstring(resp.text).xpath('//article//img[@class="post-image"]/@src')
    print('GET Url', url, len(urls), len(images))

assert len(urls) == len(images)

category = Category.objects.filter(slug='seomoz')
exists_articles = [a['source'] for a in Article.objects.filter(category=category).values('source')]
# pdb.set_trace()

for n, url in enumerate(urls):
    if url in exists_articles:
        print('Article exists', url)
        continue
    image_url = images[n][:images[n].index('?')] if '?' in images[n] else images[n]
    image_name = image_url.split('/')[-1]
    image_byte = requests.get(image_url, headers=headers).content
    with open(f'../media/images/{image_name}', 'wb') as im:
        im.write(image_byte)
    _main_img = f'images/{image_name}'
    post_img = Image.open(BytesIO(image_byte))
    resp = requests.get(url, headers=headers)
    code = resp.text.replace('&gt;', '; ').replace('&amp;', '&').replace(
        '&nbsp;', ' ').replace('& amp;', '&').replace('& nbsp', ' ')
    tree = html.fromstring(code)
    try:
        _h1 = str(tree.xpath("//h2/text()")[0])
        _post = html.tostring(tree.xpath("//div[@class='post-content']")[0], encoding='utf-8').decode('utf-8')
        _short = str(tree.xpath("//div[@class='post-content']//p/text()")[0])
        _date = dateutil.parser.parse(str(tree.xpath('//time/@datetime')[0]))

        soup = BeautifulSoup(_post, 'html.parser')
        for tag in soup.find_all():
            if tag.name not in ['iframe', 'script']:
                if tag.get('style'):
                    del(tag['style'])
                if tag.get('class'):
                    del(tag['class'])

            if tag.name == 'a':
                if tag.findChildren():
                    tag.replace_with_children()
                else:
                    tag.replace_with(tag.get_text())
            if tag.name == 'img':
                try:
                    img_name = tag['src'].split('/')[-1]
                    img_byte = requests.get('https:'+tag['src'], headers=headers).content
                    _image = Image.open(BytesIO(img_byte))
                    if _image.size[0] > post_img.size[0] and _image.size[1] > post_img.size[1]:
                        post_img = _image
                    _image.save(f'../media/images/{img_name}')
                    tag['src'] = f'/media/images/{img_name}'
                except Exception:
                    tag.replace_with('')
        soup.prettify()

        _post = str(soup).replace('<', ' <')
        _h1 = translate_text(_h1, 'en', 'ru')

        img_name = '-'.join(slugify(_h1).split('-')[:6]) + '.png'
        post_img = post_img.resize((715, 715))
        post_img.save(f'../media/images/{img_name}')
        _main_img = f'images/{img_name}'

        _short = translate_text(_short, 'en', 'ru')
        _post = translate_html(_post, 'en', 'ru')

        data = {'h1': _h1, 'post': _post, 'short': _short, 'date': _date,
                'img': _main_img, 'source': url, 'automatic': True}

        article = Article.objects.create(**data)
        article.category = category

        print('Article is saved', url)

    except Exception as e:
        print(type(e), e, 'line: ', sys.exc_info()[-1].tb_lineno)

print('All Done!')
