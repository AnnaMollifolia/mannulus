import psycopg2
import config
import sys
sys.stdout = sys.stderr


def reset_tables() -> None:
    conn = psycopg2.connect(database=config.DATABASE,
                            host=config.HOST,
                            user=config.USER,
                            password=config.PASSWORD,
                            port=config.PORT)
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS categories;")
    cur.execute("DROP TABLE IF EXISTS menu_items;")
    cur.execute("DROP TABLE IF EXISTS dishes;")
    cur.execute("""CREATE TABLE categories 
                (id SERIAL PRIMARY KEY,
                    name VARCHAR(64),
                    type VARCHAR(64));""")

    cur.execute("""CREATE TABLE menu_items 
                (id SERIAL PRIMARY KEY,
                    type VARCHAR(64),
                    name VARCHAR(128));""")

    print(" - making table ")
    cur.execute("""INSERT INTO categories (name, type) VALUES
                ('кофе','напиток'),
                ('рафы','напиток'),
                ('молоко','напиток'),
                ('не кофе','напиток'),
                ('какао','напиток'),
                ('лимонады','напиток'),
                ('молочные коктейли','напиток'),
                ('смузи','напиток'),
                ('холодный кофе','напиток'),
                ('ice-cream coffee','напиток'),
                ('new','напиток'),
                ('сиропы','сиропы'),
                ('сэндвичи','еда'),
                ('салатики','еда'),
                ('пончики','еда'),
                ('макаруны','еда'),
                ('конфеты ','еда'),
                ('фирменные товары','лишнее');""")
    conn.commit()


def get_cat_type(cat: str) -> str:
    conn = psycopg2.connect(database=config.DATABASE,
                            host=config.HOST,
                            user=config.USER,
                            password=config.PASSWORD,
                            port=config.PORT)
    cur = conn.cursor()
    cur.execute(f"SELECT type FROM categories WHERE name='{cat}';")
    return cur.fetchone()[0]


def add_item(item: str, cat: str):
    conn = psycopg2.connect(database=config.DATABASE,
                            host=config.HOST,
                            user=config.USER,
                            password=config.PASSWORD,
                            port=config.PORT)
    cur = conn.cursor()
    type = get_cat_type(cat)
    cur.execute(f"INSERT INTO menu_items(name, type) VALUES ('{item}', '{type}');")
    conn.commit()


def get_dish_items() -> list[str]:
    conn = psycopg2.connect(database=config.DATABASE,
                            host=config.HOST,
                            user=config.USER,
                            password=config.PASSWORD,
                            port=config.PORT)
    cur = conn.cursor()
    cur.execute("SELECT name FROM menu_items WHERE type='еда';")
    return [i[0] for i in cur.fetchall()]


def get_drink_items() -> list[str]:
    conn = psycopg2.connect(database=config.DATABASE,
                            host=config.HOST,
                            user=config.USER,
                            password=config.PASSWORD,
                            port=config.PORT)
    cur = conn.cursor()
    cur.execute("SELECT name FROM menu_items WHERE type='напиток';")
    return [i[0] for i in cur.fetchall()]
