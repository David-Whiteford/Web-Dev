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
    score = random.randint(0, 10)
    session["score"] = score
    return render_template(
        "score.html", the_score=score, the_title="Here is random num"
    )


@app.route("/rcordnumber", methods=["POST"])
def set_number():
    player_number= request.form["player_num"]
    player_name = request.form["player_name"]
    guess_count =0
    session["player_guess"] = guess_count
    session["player_name"] = player_name
    session["player_num"] = player_number
    return render_template(
        "playernum.html",
        the_playernum = player_number,
        )
 


@app.route("/checknum", methods=["POST"])
def check_number():
    players_score = int(session["player_num"])
    random_score = session["score"]
    guess_count = session["player_guess"]

    if players_score < random_score:
        guess_count = guess_count +1
        return render_template(
        "score.html",
        the_number="Your score is too low")
    elif players_score > random_score:
        guess_count = guess_count +1
        return render_template(
        "score.html",
        the_number="Your score is too heigh")
    elif players_score == random_score:
        player_times = session["end"] = time.perf_counter() 
        session["player_time"]  = player_times
        time_taken = round(player_times - session["start"], 2)
        session["player_time"] = time_taken
        return render_template(
        "ScoreTable.html",
        the_title="Your score is Right You win now see Highscore Table"
        
    )
    

@app.route("/addtoscoretable", methods=["POST"])
def add_to_score_table():
  
    player_name =  session["player_name"]
    player_guesses = session["player_guess"]
    player_time = session["player_time"]
  

    if not os.path.exists(FNAME):
        data = []
    else:
        with open(FNAME, "rb") as pf:
            data = pickle.load(pf)
    data.append((player_name , player_guesses, player_time))  ## RACE CONDITION.
    with open(FNAME, "wb") as pf:
        pickle.dump(data, pf)
    return render_template(
        "winner.html",
        the_title="Here are the High Scores",
        the_data=sorted(data, reverse=True),
    )
    

app.secret_key = (
    " wen'0ut93u4t0934ut93u4t09 3u4t9 u3   40tuq349tun34#-9tu3#4#vetu #    -4"
)

app.run(debug=True)
