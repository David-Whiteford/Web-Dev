from flask import Flask, render_template, session, request
import random
import os
import pickle
import time
FNAME = "data/scores.pickle"

app = Flask(__name__)


@app.route("/game")
def display_score():
    session["start"] = time.perf_counter()
    player_time = session["player_time"]
    score = random.randint(0, 10)
    session["score"] = score
    return render_template(
        "score.html", the_score=score, the_title="Here is your High Score"
    )


@app.route("/recordhighscore", methods=["POST"])
def store_score():

    player_name = request.form["player_name"]
    player_guesses = session["player_guess"]
    player_score = request.form["player_score"]
    session["player_num"] = player_score
    player_time =  session["player_time"]
    if not os.path.exists(FNAME):
        data = []
    else:
        with open(FNAME, "rb") as pf:
            data = pickle.load(pf)
    data.append((player_name , player_guesses, player_time))  ## RACE CONDITION.
    with open(FNAME, "wb") as pf:
        pickle.dump(data, pf)

    return "Your time and guess were recorded."
    


@app.route("/comparenums")
def show_scores():
    players_score = session["player_num"]
    random_score = session["score"]
    guess_count =0
    session["player_guess"] = guess_count
    if players_score < random_score:
        guess_count+1
        return render_template(
        "score.html",
        the_title="Your score is too low",
        the_data=sorted(data, reverse=True),
        return render_template("score.html")
    elif players_score > random_score:
        guess_count+1
        return render_template(
        "score.html",
        the_title="Your score is too hight",
        the_data=sorted(data, reverse=True),
        return render_template("score.html")
    elif players_score == random_score:
        player_times = session["end"] = time.perf_counter() 
        session["player_time"]  =player_times
    elif players_score == random_score:
        with open(FNAME, "rb") as pf:
        data = pickle.load(pf)
        return render_template(
        "winners.html",
        the_title="Your score is Right You win",
        the_data=sorted(data, reverse=True),
    )
    time_taken = round(session["end_time"] - session["start_time"], 2)

app.secret_key = (
    " wen'0ut93u4t0934ut93u4t09 3u4t9 u3   40tuq349tun34#-9tu3#4#vetu #    -4"
)

app.run(debug=True)
