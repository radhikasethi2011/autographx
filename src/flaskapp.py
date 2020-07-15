from utils import get_autos, split_paragraph, get_display_img

# import autographx
from flask import Flask, render_template

autos = get_autos("YearbookENTC")
app = Flask(__name__)


@app.route("/")
def homepage():
    return render_template("index.html", len=len(autos), autos=autos)

@app.route("/source/<name>")
def index_func(name):
    return render_template("whiteauto.html", len=len(autos), autos=autos, name=name) 

if __name__ == "__main__":
    app.run(use_reloader=True, debug=True)



