from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# Function to read topics from the topics.txt file
def load_topics():
    try:
        with open('ecell/topics.txt', 'r') as file:
            topics = [line.strip() for line in file if line.strip()]
        return topics
    except FileNotFoundError:
        return []

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_topics", methods=["GET"])
def get_topics():
    topics = load_topics()
    return jsonify(topics)

@app.route("/submit", methods=["POST"])
def submit():
    # Get the selected topic from the form submission
    selected_topic = request.json.get("topic")
    topics = load_topics()

    if selected_topic in topics:
        # Remove the selected topic from the file
        updated_topics = [topic for topic in topics if topic != selected_topic]
        with open('ecell/topics.txt', 'w') as file:
            for topic in updated_topics:
                file.write(topic + '\n')
        return jsonify({"message": "Topic submitted successfully.", "remaining_topics": updated_topics}), 200
    return jsonify({"message": "Topic not found."}), 400

if __name__ == "__main__":
    app.run(debug=True)
