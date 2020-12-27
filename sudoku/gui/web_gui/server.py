import time
from typing import Optional

import flask
from flask import request, jsonify, send_from_directory

from sudoku import board
from sudoku.gui.web_gui.session import Session
import random

class Game:
    session: Session

    def __init__(self):
        self.session = Session()
        self.app = flask.Flask(__name__)
        self.app.config["DEBUG"] = True


        self.app.route("/<path:path>", methods=["GET"])(self.serve_static)
        self.app.route("/api/view", methods=["POST"])(self.view)
        self.app.route("/api/new", methods=["POST"])(self.new)
        self.app.route("/api/place", methods=["POST"])(self.place)
        self.app.route("/api/undo", methods=["POST"])(self.undo)
        self.app.route("/api/implication", methods=["POST"])(self.implication)

    def serve_static(self, path):
        return send_from_directory("./static/", path)

    def new(self):
        key = int(time.time() + random.randrange(0, 2**32)) % 2**32
        self.session.set(key, board.Game(key))
        return jsonify({
            "key": key,
        })

    def implication(self):
        '''
        {
            row: int,
            col: int,
            value: int
        }
        '''
        try:
            body = request.json
            key = body["key"]
            board_game = self.session.get(key)
            implication = board_game.implication()
            if implication is None:
                return jsonify(None)
            return jsonify(implication.marshal())
        except Exception:
            return jsonify(), 400

    def view(self):
        '''
        {
            youwin: bool,
            current_board: list of list of int,
            initial_mask: list of list of bool,
            violation_mask: list of list of bool,
        }
        '''
        try:
            body = request.json
            key = body["key"]
            board_game = self.session.get(key)
            return jsonify(board_game.view().marshal())
        except Exception:
            return jsonify(), 400

    def place(self):
        '''
        {
            "row": 1,
            "col": 2,
            "value": 3,
        }
        '''
        try:
            body = request.json
            key = body["key"]
            board_game = self.session.get(key)
            row, col = body["row"], body["col"]
            value = body.get("value", 0)
            board_game.place(row, col, value)
            return jsonify()
        except Exception:
            return jsonify(), 400

    def undo(self):


        try:
            body = request.json
            key = body["key"]
            board_game = self.session.get(key)
            undo = board_game.undo()
            if undo is None:
                return jsonify(None)
            return jsonify(undo.marshal())
        except Exception:
            return jsonify(), 400

    def run(self, *args, **kwargs):
        self.app.run(*args, **kwargs)
