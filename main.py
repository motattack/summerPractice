from module.category import parse_category, categorize
from module.common import stopwatch, save_json, load_json, delete_cvs
from module.product import pagination_loop
from module.request import get_html

DEBUG = False


@stopwatch
def main():
    if not DEBUG:
        html = get_html('https://es14.ru', '/catalog/')
        res = parse_category(html, site='https://es14.ru')
        save_json("categories.json", res)
    else:
        res = load_json('categories.json')
    categorize(res)
    main_categories = load_json('main_cat.json')
    delete_cvs()
    for key in main_categories:
        pagination_loop(main_categories[key], True)


if __name__ == "__main__":
    main()
