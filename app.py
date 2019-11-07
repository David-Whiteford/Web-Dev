from flask import Flask, render_template, session, request
import random
import os
import pickle

FNAME = "data/scores.pickle"

app = Flask(__name__)


@app.route("/game")
def display_score():
    score = random.randint(0, 100)
    session["score"] = score
    return render_template(
        "score.html", the_score=score, the_title="Here is your High Score"
    )


@app.route("/recordhighscore", methods=["POST"])
def store_score():
    score = session["score"]

    player_score = request.form["player_score"]

    if not os.path.exists(FNAME):
        data = []
    else:
        with open(FNAME, "rb") as pf:
            data = pickle.load(pf)
    data.append((player_score , score))  ## RACE CONDITION.
    with open(FNAME, "wb") as pf:
        pickle.dump(data, pf)

    return "Your highscore has been recorded."


@app.route("/showhighscores")
def show_scores():
    with open(FNAME, "rb") as pf:
        data = pickle.load(pf)
    return render_template(
        "winners.html",
        the_title="Here are the High Scores",
        the_data=sorted(data, reverse=True),
    )


app.secret_key = (
    " wen'0ut93u4t0934ut93u4t09 3u4t9 u3   40tuq349tun34#-9tu3#4#vetu #    -4"
)

app.run(debug=True)
