from flask import Flask, jsonify
from flask_cors import CORS
from aiMain import test
from oddsScraper import scraper
from saveData import linker
# import your_list_generator_script

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def getStats():
    players = test(0, False)

    for i in range(len(players)):
        players[i] = players[i]['player']

    playerInfo = scraper()

    linker(players, playerInfo)

    jsonPlayers = []
    for p in players:
        jsonPlayers.append(p.toJSON())

    return jsonPlayers

jsonPlayers = None

@app.route('/api/list', methods=['GET'])
def get_list():
    return jsonify(jsonPlayers)

if __name__ == '__main__':
    jsonPlayers = getStats()
    app.run(debug=True)
