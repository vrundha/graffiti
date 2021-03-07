from flask import Flask, request
from flask_restful import Resource, Api
import psycopg2
from semantics import Semantics
from collections import Counter
import numpy as np
import time
from flask_cors import CORS

app = Flask(__name__, static_url_path='',
            static_folder='graffiti_front_end/',
            template_folder='')
CORS(app)

api = Api(app)

db_server_uri = "postgresql://root@localhost:26257?sslcert=certs%2Fclient.root.crt&sslkey=certs%2Fclient.root.key" \
                "&sslmode=verify-full&sslrootcert=certs%2Fca.crt"

conn = psycopg2.connect(db_server_uri)
semantics = Semantics()


class Graffiti(Resource):
    def __init__(self):

        with conn.cursor() as cur:
            # cur.execute("CREATE USER vru WITH PASSWORD 'cockroach'")
            # cur.execute("GRANT admin TO vru")
            cur.execute("CREATE DATABASE IF NOT EXISTS social")
            cur.execute("CREATE TABLE IF NOT EXISTS social.graffiti (emotion STRING, comment STRING)")
            conn.commit()

    def insert(self):
        with conn.cursor() as cur:
            cur.execute("DELETE FROM social.graffiti")
            rows = [["sad", "my wife is leaving me"], ["sad", "my husband and I are getting separated"], ["sad", "I'm getting divorced"],
                    ["sad", "I failed my test"], ["sad", "I got bad scores in my test"],
                    ["sad", "My wife broke my heart"], ["sad", "My wife is cheating on me!"],
                    ["sad", "mother passed away due to covid"],
                    ["happy", "I'm pregnant"], ["happy", "I'm having a baby"],
                    ["happy", "I won in a hackathon!"], ["happy", "I got first place in a hackathon"],
                    ["happy", "wonderful trip to malaysia"], ["happy", "I love my family"],
                    ["happy", "I bought a new car"], ["happy", "I love my car"],
                    ["calm", "exercising"], ["calm", "taking a nap in my room"], ["calm", "at the sea"], ["calm", "at the mountains"],
                    ["angry", "so much corruption in the world"], ["angry", "deaths due to covid"], ["angry", "lockdown due to covid"],
                    ["angry", "can't meet friends due to pandemic"], ["angry", "activities are shut due to covid"],
                    ["angry", "lockdown"], ["angry", "lockdown"], ["angry","I lost a game"]
                    ]
            for row in rows:
                cur.execute("INSERT INTO social.graffiti(emotion, comment) VALUES(%s, %s)", (row[0], row[1]))
            conn.commit()

    def cluster_counter(self, comments, cluster_labels):
        frequency = []
        result = []
        frequency = Counter(cluster_labels)
        for (key, value) in frequency.items():
            i = np.where(cluster_labels == key)[0]
            i = np.random.choice(i, size=1)
            result.append([comments[int(i)], value])
        return result

    def get(self):
        # self.insert()
        _start = time.time()
        with conn.cursor() as cur:
            # print(time.time()-_start)
            cur.execute("SELECT emotion, comment FROM social.graffiti")
            rows = cur.fetchall()
            conn.commit()
            comments = {}
            cluster_labels = {}
            frequency = {}
            # print(time.time()-_start, "Starting clustering")
            for emotion in ["happy", "sad", "calm", "angry"]:
                comments[emotion], cluster_labels[emotion] = semantics.cluster(rows, emotion)
                frequency[emotion] = self.cluster_counter(comments[emotion], cluster_labels[emotion])
            # print(time.time() - _start, "Stopping clustering")
            return frequency

        # return rows

    def post(self):
        # text = request.form['text']
        emo = request.form['emo'].lower()
        comm = request.form['comm']

        # print(emo, comm)
        with conn.cursor() as cur:
            cur.execute("INSERT INTO social.graffiti(emotion, comment) VALUES(%s, %s)", (emo, comm))
            conn.commit()
            return {"success": True}


api.add_resource(Graffiti, "/graffiti")


@app.route('/')
def static_file():
    return app.send_static_file("index.html")


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, threaded=True, debug=True)
