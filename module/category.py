from dataclasses import dataclass, asdict

from module.common import save_json, calculate_hash
from module.request import extract, get_html


@dataclass
class Category:
    id: int
    name: str
    url: str
    children: list


def parse_category(html, indent_level=0, site='https://example.com'):
    if html is not None:
        categories = []
        for item in html.css('.catalog-section-list-item'):
            if extract(item, '.catalog-section-list-item-title-depth', 'attrs'):
                name = extract(item, '.catalog-section-list-item-title-depth', 'attrs')['title']
            else:
                full_name = extract(item, 'h3.catalog-section-list-item-title', 'text')
                item_count = extract(item, 'span.catalog-section-list-item-counter', 'text')
                name = full_name.replace(item_count, '')

            path = extract(item, 'a', 'attrs')['href']

            indentation = ' ' * (indent_level * 4)
            print(f"{indentation}{name} -> {path}")

            category = Category(
                id=calculate_hash(path),
                name=name,
                url=site + path,
                children=parse_category(get_html(site, path), indent_level + 1, site)
            )
            categories.append(asdict(category))
        return categories
    return []


def flatten_category_tree(tree, result_dict):
    for category in tree:
        name = category['name']
        category_id = category['id']
        url = category['url']
        result_dict[category_id] = [name, url]
        if 'children' in category:
            flatten_category_tree(category['children'], result_dict)


def main_category(tree, result_dict):
    for category in tree:
        name = category['name']
        category_id = category['id']
        url = category['url']
        result_dict[category_id] = [name, url]


def categorize(category_tree):
    flattened_dict = {}
    flatten_category_tree(category_tree, flattened_dict)

    main_dict = {}
    main_category(category_tree, main_dict)

    save_json("categorize.json", flattened_dict)
    save_json("main_cat.json", main_dict)
