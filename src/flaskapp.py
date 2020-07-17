from utils import get_autos, split_paragraph, get_display_img
from flask import request

# import autographx
from flask import Flask, render_template


#for x,y in autos[0]['autographs'].items():  to print name : autograph 
#...     print(x, " : ", y)


autos = get_autos("YearbookENTC")
app = Flask(__name__)


@app.route("/")
def homepage():
    return render_template("index.html", len=len(autos), autos=autos)

@app.route("/autographs/<string:name>")
def index_func(name):
    my_var = request.args.get('my_var',None)
    return """<h1> the name is : {}</h1>""".format(my_var)
    #return render_template("whiteauto.html", len=len(autos), autos=autos, my_var=my_var) 

if __name__ == "__main__":
    app.run(use_reloader=True, debug=True)



