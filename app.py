from flask import Flask, jsonify, request

app = Flask(__name__)


class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {"id": self.id, "title": self.title}


events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop"),
]


def find_event(event_id):
    for event in events:
        if event.id == event_id:
            return event
    return None


@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Welcome to the Events API!"}), 200


@app.route("/events", methods=["GET"])
def list_events():
    return jsonify([event.to_dict() for event in events]), 200


@app.route("/events", methods=["POST"])
def create_event():
    data = request.get_json(silent=True) or {}
    title = data.get("title")

    if not title:
        return jsonify({"error": "Title is required"}), 400

    next_id = max((event.id for event in events), default=0) + 1
    new_event = Event(next_id, title)
    events.append(new_event)
    return jsonify(new_event.to_dict()), 201


@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
    data = request.get_json(silent=True) or {}
    title = data.get("title")

    if not title:
        return jsonify({"error": "Title is required"}), 400

    event = find_event(event_id)
    if event is None:
        return jsonify({"error": "Event not found"}), 404

    event.title = title
    return jsonify(event.to_dict()), 200


@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    event = find_event(event_id)
    if event is None:
        return jsonify({"error": "Event not found"}), 404

    events.remove(event)
    return "", 204


if __name__ == "__main__":
    app.run(debug=True)
