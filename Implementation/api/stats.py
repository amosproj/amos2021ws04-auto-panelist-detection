import csv
from flask import Flask, jsonify


app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False


@app.get("/")
def get_stats():
    stats = []
    with open("logs.csv", newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            stats.append({'timestamp': row['timestamp'], 'id': row['id'], 'gender': row['gender'], 'age': row['age'],
                          'emotion': row['emotion'], 'attentiveness': row['attentiveness']})

    return jsonify(stats)


def start_api():
    app.run()
