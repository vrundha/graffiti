from sentence_transformers import SentenceTransformer, util
import numpy as np
from sklearn.cluster import AgglomerativeClustering
import time


class Semantics:
    def __init__(self):
        self.model = SentenceTransformer('stsb-roberta-large')

    def get_comments_with_sentiment(self, rows, sentiment):
        result = []
        for row in rows:
            print(row, sentiment, row[0] == sentiment)
            if row[0] == sentiment:
                result.append(row[1])
        return result

    def cluster(self, rows, sentiment):
        print(rows)
        comments = self.get_comments_with_sentiment(rows, sentiment)
        print(time.time(), comments)
        embedding = self.model.encode(comments, convert_to_tensor=True)  # store this in db
        print(time.time())
        clustering = AgglomerativeClustering(n_clusters=None, distance_threshold=30).fit(embedding)
        print(time.time())
        return comments, clustering.labels_  # , clustering.distances_


if __name__ == "__main__":
    sem = Semantics()
    _rows = [["sad", "My wife is leaving me"], ["sad", "committing suicide"], ["sad", "I getting divorced"], ["sad", "my wife broke my heart"], ["sad", "My wife is cheating on me!"]]
    print(sem.cluster(_rows,"sad"))





