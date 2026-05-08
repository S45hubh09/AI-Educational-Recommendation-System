from flask import Flask, render_template, request
from youtube_api import get_videos
from Ranking_videos import ranking

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/recommend', methods=['POST'])
def recommend():
    topic = request.form['topic']
    level = request.form['level']

    if level == "Beginner":
        topic += " beginner tutorial"
    elif level == "Intermediate":
        topic += " intermediate tutorial"
    else:
        topic += " advanced tutorial"

    try:
        videos = get_videos(topic)

        if len(videos) == 0:
            return render_template("Error_Msg.html", topic=topic)

        videos = ranking(videos)

        return render_template(
            'result.html',
            topic=topic,
            level=level,
            videos=videos,
        )

    except Exception as e:
        print("ERROR:", e)
        return f"Error: {e}"


# ✅ Correct video route
@app.route('/video/<video_id>')
def play_video(video_id):
    return render_template('Video_player.html', video_id=video_id)


if __name__ == '__main__':
    app.run(debug=True, port=5001)