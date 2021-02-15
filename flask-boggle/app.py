from flask import Flask, request, render_template, jsonify, session
from boggle import Boggle

app = Flask(__name__)
app.config["SECRET_KEY"] = "fdfgkjtjkkg45yfdb"

boggle_game = Boggle()


@app.route("/")
def homepage():
    """Generate the game board."""

    board = boggle_game.make_board()
    session['board'] = board
    highscore = session.get("highscore", 0)
    timesplayed = session.get("nplays", 0)

    return render_template("index.html", board=board, highscore=highscore, timesplayed=timesplayed)


@app.route("/check-word")
def check_word():
    """Check if user's input word exists in the dictionary."""

    word = request.args["word"]
    board = session["board"]
    response = boggle_game.check_valid_word(board, word)

    return jsonify({'result': response})


@app.route("/post-score", methods=["POST"])
def post_score():
    """Receives the score, and updates the highscore if it's beaten, and checks the number of times played."""

    score = request.json["score"]
    highscore = session.get("highscore", 0)
    timesplayed = session.get("timesplayed", 0)

    session['timesplayed'] = timesplayed + 1
    session['highscore'] = max(score, highscore)

    return jsonify(brokeRecord=score > highscore)
