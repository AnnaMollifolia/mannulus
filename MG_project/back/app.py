import flask
import scraper
from apscheduler.schedulers.background import BackgroundScheduler
import random
import db

import sys
sys.stdout = sys.stderr

DO_INIT_SCRAPE = True

app = flask.Flask(__name__)


@app.route("/bestset", methods=['get'])
def bestset():
    dishes = db.get_dish_items()
    drinks = db.get_drink_items()
    return flask.jsonify({
        "drink": random.choice(drinks),
        "dish": random.choice(dishes)
    })


if __name__ == "__main__":
    if DO_INIT_SCRAPE:
        scraper.scrape()
    s = BackgroundScheduler()
    s.add_job(func=scraper.scrape, trigger='interval', hours=24)
    s.start()
    app.run("0.0.0.0", "6000")
