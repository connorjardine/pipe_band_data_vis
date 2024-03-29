from flask import Flask

from blueprints.worlds_blueprint import *
from blueprints.dashboard_blueprint import *
from blueprints.major_wins_blueprint import *
from blueprints.band_results_blueprint import *

app = Flask(__name__)

app.register_blueprint(dashboard)
app.register_blueprint(worlds)
app.register_blueprint(major_wins)
app.register_blueprint(band_results)

if __name__ == "__main__":
    app.run(host="0.0.0.0")



