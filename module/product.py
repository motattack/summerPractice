from dataclasses import dataclass, asdict
from urllib.parse import urljoin

from selectolax.parser import HTMLParser

from module.common import clear_price, calculate_hash, delete_cvs, to_csv
from module.request import extract, get_html


@dataclass
class Product:
    id: int
    name: str
    price: str
    old_price: str
    category: int
    content: str
    image_url: str


product_fields = ['id', 'name', 'price', 'old_price', 'category', 'content', 'image_url']


@dataclass
class Response:
    body_html: HTMLParser
    next_page: dict


def get_page(url, debug=False):
    html = get_html(url, '')

    if debug:
        print(f'[info] product link: ', url)

    if html.css_first('li.bx-pag-next > a'):
        next_page = html.css_first('li.bx-pag-next > a').attributes
    else:
        next_page = {"href": False}
    return Response(body_html=html, next_page=next_page)


def parse_detail(html, link, base_url):
    new_product = Product(
        id=calculate_hash(link),
        name=extract(html, ".bx-catalog-element > h1", "text"),
        price=clear_price(extract(html, '.product-item-detail-price-current', "text")),
        old_price=clear_price(extract(html, '.product-item-detail-price-old', "text")),
        category=extract(html, '.bx-breadcrumb-item > a', 'hash', -2),
        content=extract(html, '.product-item-detail-tab-content', 'text'),
        image_url=base_url + extract(html, '.product-item-detail-slider-image > img', 'attrs')['src'],
    )
    return new_product


def detail_page_loop(page, debug=False):
    base_url = 'https://es14.ru'
    products = []
    for link in parse_links(page.body_html):
        detail_page = get_page(urljoin(base_url, link), debug)
        product = parse_detail(detail_page.body_html, link, base_url)
        products.append(asdict(product))
    return products


def parse_links(html):
    links = html.css('div.product-item > a')
    return {link.attrs['href'] for link in links}


def pagination_loop(data, debug=False):
    delete_cvs()

    if debug:
        print(f'[info] start "{data[0]}"')
    url = data[1]

    while True:
        page = get_page(url)
        products = detail_page_loop(page)
        if page.next_page['href'] is False:
            break
        else:
            url = urljoin(url, page.next_page['href'])
            if debug:
                print(f'[info] page {page.next_page["href"]}')
        to_csv(products, product_fields)
