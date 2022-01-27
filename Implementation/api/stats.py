import csv

from flask import Flask, jsonify

app = Flask(__name__)

@app.get("/stats")
def get_stats():
    stats = []
    with open("Implementation/logs.csv", newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            stats.append({'timestamp': row['timestamp'], 'gender': row['gender'], 'age': row['age'], 'emotion': row['emotion']})

    return jsonify(stats)

