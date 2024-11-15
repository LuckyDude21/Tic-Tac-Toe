from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Játékállapot
game_board = [["" for _ in range(3)] for _ in range(3)]
current_player = "X"

def check_winner():
    """Győzelem ellenőrzése."""
    # Sorok
    for row in game_board:
        if row[0] == row[1] == row[2] and row[0] != "":
            return row[0]

    # Oszlopok
    for col in range(3):
        if game_board[0][col] == game_board[1][col] == game_board[2][col] and game_board[0][col] != "":
            return game_board[0][col]

    # Átlók
    if game_board[0][0] == game_board[1][1] == game_board[2][2] and game_board[0][0] != "":
        return game_board[0][0]
    if game_board[0][2] == game_board[1][1] == game_board[2][0] and game_board[0][2] != "":
        return game_board[0][2]

    return None

def is_draw():
    """Döntetlen ellenőrzése."""
    for row in game_board:
        if "" in row:
            return False
    return True

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/move", methods=["POST"])
def move():
    global current_player
    data = request.json
    row, col = data["row"], data["col"]

    if game_board[row][col] != "":
        return jsonify({"error": "Cell is already taken!"}), 400

    game_board[row][col] = current_player
    winner = check_winner()
    if winner:
        return jsonify({"winner": winner})

    if is_draw():
        return jsonify({"draw": True})

    current_player = "O" if current_player == "X" else "X"
    return jsonify({"success": True, "currentPlayer": current_player})

if __name__ == "__main__":
    app.run(debug=True)
