from flask import Flask, request, jsonify
from rasa.core.agent import Agent

app = Flask(__name__)
agent = Agent.load("C:/Users/User/Documents/School/Sem 5/AI/apspace-chatbot/models/20240205-001431-lively-plasma.tar.gz")


@app.route("/")
def hello():
    return "Hello, this is your Flask server!"

if __name__ == "__main__":
    app.run(debug=True)

