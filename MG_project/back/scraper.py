import bs4
import re
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
import db

# docker-compose loses stdout
import sys
sys.stdout = sys.stderr

NUMBER_PATTERN = re.compile("[0-9]+")


def save_category(items: list[str], cat: str):
    print(f"-saving category {cat}")
    for item in items:
        print(f" - {item}")
        db.add_item(f"{cat} - {item}", cat)


def extract_menu(data: str):
    title_tags = data.find_all('div', {"style": "line-height: 62px;"})
    title_tags += data.find_all('div', {"style": "line-height: 53px;"})
    titles = [t.decode_contents().lower()for t in title_tags]
    item_tags: list[bs4.Tag] = data.find_all('div', {"style": "line-height: 27px;"})
    item_tags += data.find_all('div', {"style": "line-height: 22px;"})
    item_tags += data.find_all('div', {"style": "line-height: 24px;"})
    print('2', item_tags)
    has_br = any(("<br/>" in item.decode_contents()) for item in item_tags)
    has_li = any(("<li>" in item.decode_contents()) for item in item_tags)
    if has_li and has_br:
        ti: list[list[str]] = [tag.decode_contents()[8:-10].lower().split("</li><li>") for tag in item_tags]
        items = []
        for ni in ti:
            item = []
            print(ni)
            for i in item:
                if "<br/>" in i:
                    item += i.split("<br/>")
                else:
                    item.append(i)
            items.append(item)

        # items = [flatten(item.split()) for item in items]
    elif has_br:
        items = [tag.decode_contents().lower().split("<br/>") for tag in item_tags]
    elif has_li:
        items = [tag.decode_contents()[8:-10].lower().split("</li><li>") for tag in item_tags]
    print(f"{titles = }")
    print(f"{items = }")
    if not items:
        print(data)
    for i in range(min(len(items), len(titles))):
        save_category(items[i], titles[i])


def scrape():
    db.reset_tables()
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--headless=new")
    options.add_argument('--start-maximized')

    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
    print("starting driver")
    with Chrome(options=options) as driver:
        print("starting working")
        url = "https://monkey-grinder.ru"
        driver.get(url)
        page_soup = bs4.BeautifulSoup(driver.page_source, 'html.parser')

        group_1: list[bs4.Tag] = page_soup.find_all('div', attrs={
            "class": "t396__artboard rendered",
            "data-artboard-height": "680",
            "data-artboard-height-res-320": "425"})

        group_cofee = page_soup.find('div', attrs={
            "class": "t396__artboard rendered",
            "data-artboard-height": "691",
            "data-artboard-height-res-320": "425"})
        for group in group_1:
            extract_menu(group)
        extract_menu(group_cofee)


"""
div class="t396__artboard rendered" data-artboard-height="680" data-artboard-height-res-320="425">
для не кофе, еда, сезонное, новинки, фирманные товары

<div class="t396__artboard rendered" data-artboard-height="691" data-artboard-height-res-320="425">

для кофе

"""
