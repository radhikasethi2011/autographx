from utils import get_autos, split_paragraph, get_display_img
from flask import request

# import autographx
from flask import Flask, render_template


#for x,y in autos[0]['autographs'].items():  to print name : autograph 
#...     print(x, " : ", y)



app = Flask(__name__)


@app.route("/")
def homepage():
    return render_template("index.html", len=len(autos), autos=autos)

@app.route("/autographs/<string:name>")
def index_func(name):
    #my_var = request.args.get('name',None)
    #return """<h1> the name is : {}</h1>""".format(name)
    return render_template("whiteauto.html", len=len(autos), autos=autos, name=name) 

if __name__ == "__main__":
    autos = get_autos("YearbookENTC", download_image=False)
    app.run(use_reloader=True, debug=True)



