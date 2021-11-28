from os import listdir,getcwd,chdir,system,remove
from flask import Flask,request,render_template


app = Flask(__name__)


@app.route("/",methods=["GET","POST"])
def index():

    chdir("../tests")

    lst = [x for x in listdir(getcwd()) if x.startswith("test")]

    lst = [x.split(".")[0].split('_')[-1] for x in lst]


    if request.method == "POST":

        tests_active = request.form.getlist("mycheckbox")

        dict = {}

        for x in tests_active:

            system(f"pytest test_{x}.py -v > {x}.txt")

            with open(f"{x}.txt") as f:
                result_file = f.read()


            dict.update({x:"failed_test"}) if "AssertionError" in result_file else dict.update({x:"passed_test"})


            remove(f"{x}.txt")


        return render_template("result_test.html",dict=dict)


    return render_template("index.html",lst=lst)

if __name__ == "__main__":
    app.run(debug=True)