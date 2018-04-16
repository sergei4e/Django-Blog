import sys
import os
import django
import pdb
import requests
from io import BytesIO
from PIL import Image
from lxml import html
import dateutil.parser
from bs4 import BeautifulSoup
from urllib.parse import unquote


P = os.path.abspath(__file__)
P = os.path.dirname(P)
P = os.path.dirname(P)
sys.path.append(P)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "seoshnik.settings")
django.setup()

from blog.models import Article, Category

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:50.0) Gecko/20100101 Firefox/50.0'}

main_url = 'http://сеошник.укр/'
resp = requests.get(main_url, headers=headers)
urls = html.fromstring(resp.text).xpath('//h2/a/@href')
images = html.fromstring(resp.text).xpath('//article//img/@src')

category = Category.objects.filter(slug='my-articles')
exists_articles = [a['source'] for a in Article.objects.filter(category=category).values('source')]
# pdb.set_trace()

for n, url in enumerate(urls):
    if url in exists_articles:
        print('Article exists', url)
        continue
    image_url = images[n]
    image_name = image_url.split('/')[-1]
    image_byte = requests.get(image_url, headers=headers).content
    with open(f'../media/images/{image_name}', 'wb') as im:
        im.write(image_byte)

    _main_img = f'images/{image_name}'
    post_img = Image.open(BytesIO(image_byte))
    resp = requests.get(url, headers=headers)
    tree = html.fromstring(resp.text)
    try:
        _h1 = str(tree.xpath("//h1/text()")[0])
        _post = html.tostring(tree.xpath("//div[contains(@class, 'post_content')]")[0])
        _short = str(tree.xpath("//p/text()")[0])
        _date = dateutil.parser.parse(str(tree.xpath('//time/@datetime')[0]))
        _img = f'images/{image_name}'

        soup = BeautifulSoup(_post, 'html.parser')
        for tag in soup.find_all():
            if tag.name not in ['iframe', 'script']:
                if tag.get('style'):
                    del(tag['style'])
                if tag.get('class'):
                    del(tag['class'])

            # if tag.name == 'a':
            #     if tag.findChildren():
            #         tag.replace_with_children()
            #     else:
            #         tag.replace_with(tag.get_text())
            if tag.name == 'img':
                try:
                    src = unquote(tag['src'])
                    img_name = src.split('/')[-1]
                    img_byte = requests.get(src, headers=headers).content
                    _image = Image.open(BytesIO(img_byte))
                    if _image.size[0] > post_img.size[0] and _image.size[1] > post_img.size[1]:
                        _main_img = f'images/{img_name}'

                    with open(f'../media/images/{img_name}', 'wb') as im:
                        im.write(img_byte)
                    tag['src'] = f'/media/images/{img_name}'
                except Exception as e:
                    print(type(e), e, 'line: ', sys.exc_info()[-1].tb_lineno)
                    tag.replace_with('')
        soup.prettify()
        _post = str(soup).replace('<', ' <')

        img = Image.open(f'../media/{_main_img}')
        img2 = img.resize(img.size)
        while True:
            if img2.size[0] > 600 and img2.size[1] > 600:
                break
            img2 = img2.resize((img2.size[0]*2, img2.size[1]*2))

        img2.save(f'../media/{_main_img}')

        # with open(f'../media/{_main_img}', 'wb') as im:
        #    im.write(img_byte)

        data = {'h1': _h1, 'post': _post, 'short': _short, 'date': _date, 'img': _main_img}

        article = Article.objects.create(**data)
        article.category = category

        print('Article is saved', url)
        # pdb.set_trace()

    except Exception as e:
        print(type(e), e, 'line: ', sys.exc_info()[-1].tb_lineno)

print('All Done!')
