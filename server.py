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
            cur.execute("CREATE DATABASE IF NOT EXISTS social")
            cur.execute("CREATE TABLE IF NOT EXISTS social.graffiti (emotion STRING, comment STRING)")
            conn.commit()

    def insert(self):
        with conn.cursor() as cur:
            cur.execute("DELETE FROM social.graffiti")
            rows = [["sad", "My wife is leaving me"], ["sad", "committing suicide"], ["sad", "my husband is leaving me"],
                    ["sad", "I failed"], ["sad", "I'm getting divorced"],
                    ["sad", "My wife broke my heart"], ["sad", "My wife is cheating on me!"], ["happy", "I'm married"], ["happy", "I passed!"]]
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
            print(time.time()-_start)
            cur.execute("SELECT emotion, comment FROM social.graffiti")
            rows = cur.fetchall()
            conn.commit()
            comments = {}
            cluster_labels = {}
            frequency = {}
            print(time.time()-_start, "Starting clustering")
            for emotion in ["happy", "sad"]:
                comments[emotion], cluster_labels[emotion] = semantics.cluster(rows, emotion)
                frequency[emotion] = self.cluster_counter(comments[emotion], cluster_labels[emotion])
            print(time.time() - _start, "Stopping clustering")
            return frequency

        # return rows

    def post(self):
        # text = request.form['text']
        emo = request.form['emo']
        comm = request.form['comm']

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
