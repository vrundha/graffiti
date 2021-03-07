from flask import Flask, request
from flask_restful import Resource, Api
import psycopg2
from semantics import Semantics
from collections import Counter
import numpy as np

app = Flask(__name__)
api = Api(app)

db_server_uri = "postgresql://root@localhost:26257?sslcert=certs%2Fclient.root.crt&sslkey=certs%2Fclient.root.key" \
                "&sslmode=verify-full&sslrootcert=certs%2Fca.crt"


class Graffiti(Resource):


    def __init__(self):
        self.conn = psycopg2.connect(db_server_uri)
        with self.conn.cursor() as cur:
            cur.execute("CREATE DATABASE IF NOT EXISTS social")
            cur.execute("CREATE TABLE IF NOT EXISTS social.graffiti (emotion STRING, comment STRING)")
            self.conn.commit()
        self.semantics = Semantics()

    def insert(self):
        with self.conn.cursor() as cur:
            cur.execute("DELETE FROM social.graffiti")
            rows = [["sad", "My wife is leaving me"], ["sad", "committing suicide"], ["sad", "my husband is leaving me"],
                    ["sad", "I failed"], ["sad", "I'm getting divorced"],
                    ["sad", "My wife broke my heart"], ["sad", "My wife is cheating on me!"], ["happy", "I'm married"], ["happy", "I passed!"]]
            for row in rows:
                cur.execute("INSERT INTO social.graffiti(emotion, comment) VALUES(%s, %s)", (row[0], row[1]))
            self.conn.commit()

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
        with self.conn.cursor() as cur:
            cur.execute("SELECT emotion, comment FROM social.graffiti")
            rows = cur.fetchall()
            self.conn.commit()
            comments = {}
            cluster_labels = {}
            frequency = {}
            for emotion in ["happy", "sad"]:
                comments[emotion], cluster_labels[emotion] = self.semantics.cluster(rows, emotion)
                frequency[emotion] = self.cluster_counter(comments[emotion], cluster_labels[emotion])

            return frequency

        # return rows

    def post(self):
        # text = request.form['text']
        emo = "sad"  # request.form['emo']
        comm = request.form['comm']

        with self.conn.cursor() as cur:
            cur.execute("INSERT INTO social.graffiti(emotion, comment) VALUES(%s, %s)", (emo, comm))
            self.conn.commit()
            return {"success": True}



api.add_resource(Graffiti, "/graffiti")

if __name__ == '__main__':
    app.run(debug=True)
