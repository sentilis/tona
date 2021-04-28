from flask import Flask, render_template
from models.objective import Objective
from models.keyresult import KeyResult

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/okr")
def okr():
    Objective.get_unarchived()
    return render_template("okr.html",
                            objectives=Objective.get_unarchived())

@app.route("/okr/<objective_id>")
def objective_detail(objective_id):
    rows = Objective.exists(objective_id)
    rows2 = KeyResult.select(KeyResult.active==True).join(Objective).where(Objective.id==objective_id)
    for a in rows2:
        print(a)

    return render_template("okr_detail.html",
                            objective=rows[0], keyresults=rows2)