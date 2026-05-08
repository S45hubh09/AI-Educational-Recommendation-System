import pandas as pd
from textblob import TextBlob


def calculate_sentiment(comments):
    if not comments or len(comments) == 0:
        return 0

    total = 0
    for c in comments:
        try:
            total += TextBlob(c).sentiment.polarity
        except:
            total += 0

    return total / len(comments)


def ranking(videos):
    df = pd.DataFrame(videos)


    df["views"] = df["views"].replace(0, 1)

    df["like_ratio"] = df["likes"] / df["views"]

    df["sentiment"] = df["comments"].apply(calculate_sentiment)

    import numpy as np

    df["score"] = (
            0.4 * df["like_ratio"] +
            0.3 * df["sentiment"] +
            0.3 * np.log1p(df["views"])
    )
    df = df.sort_values(by="score", ascending=False)

    return df.to_dict(orient="records")