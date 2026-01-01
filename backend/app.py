from flask import Flask, request, jsonify
from flask_cors import CORS
from pypresence import Presence
import os
from dotenv import load_dotenv
import time
import re

load_dotenv()
app = Flask(__name__)
CORS(app)  # Allows the extension to talk to this server

# Discord RPC Setup
APPLICATION_ID = os.getenv("APPLICATION_ID")
RPC = Presence(APPLICATION_ID)
try:
    RPC.connect()
    print("Connected to Discord!")
except Exception as e:
    print(f"Could not connect to Discord: {e}")


@app.route('/update', methods=['POST'])
def update_presence():
    data = request.get_json()
    url = data['url']
    print(url)
    if not re.search("^https://www\.chess\.com", url):
        RPC.clear()
    elif re.search("^https://www\.chess\.com/puzzles/*", url):
        RPC.update(
            details="Chess.com",
            state="Solving Puzzles",
            large_image="chess-com-icon",
            start=int(time.time())
        )
    elif re.search("^https://www\.chess\.com/game/live/*", url):
        RPC.update(
            details="Chess.com",
            state="Viewing a game",
            large_image="chess-com-icon",
            start=int(time.time())
        )

    elif re.search("^https://www\.chess\.com/game/*", url):
        RPC.update(
            details="Chess.com",
            state="In a game",
            large_image="chess-com-icon",
            start=int(time.time())
        )

    else:
        RPC.update(
            details="Chess.com",
            state="Idling",
            large_image="chess-com-icon",
            start=int(time.time())
        )
    return jsonify({"status": "success"}), 200


if __name__ == '__main__':
    app.run(port=5000)
