#!/usr/bin/env python
# -*- encoding: utf-8 -*-


from flask import Flask, jsonify, request
from flask_cors import CORS


app = Flask(__name__)
app.config.from_object(__name__)

CORS(app, resources={r"/*": {"origins": "*"}})

@app.route("/ping", methods=["GET"])
def ping_pong():
    return jsonify("pong")

BOOKS = [
    {
        'title': 'On the Road',
        'author': 'Jack Kerouac',
        'read': True
    },
    {
        'title': 'Harry Potter and the Philosopher\'s Stone',
        'author': 'J. K. Rowling',
        'read': False
    },
    {
        'title': 'Green Eggs and Ham',
        'author': 'Dr. Seuss',
        'read': True
    }
]

@app.route("/books", methods=["GET", "POST"])
def all_books():
    response_object = {"status": "success"}
    if request.method == "POST":
        post_data = request.get_json()
        BOOKS.append({
            "title": post_data.get("title"),
            "author": post_data.get("author"),
            "read": post_data.get("read")
        })
        response_object["message"] = "BOOK added!"
    else:
        response_object["books"] = BOOKS
    return jsonify(response_object)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
