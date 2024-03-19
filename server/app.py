from flask import Flask, jsonify, request, current_app
from flask.json.provider import DefaultJSONProvider
from sqlalchemy import create_engine, text


class CustomJSONEncoder(DefaultJSONProvider):
    def __init__(self, application):
        super().__init__(application)

    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)

        return list(obj)


def create_app(test_config = None):
    app = Flask(__name__)

    if test_config is None:
        app.config.from_pyfile("config.py")
    else:
        app.config.update(test_config)

    print(app.config['DB_URL'])

    database = create_engine(
        app.config['DB_URL'],
        # encoding='utf-8',
        max_overflow=0
    )

    app.database = database

    return app


app = create_app()


@app.route("/sign-up", methods=['POST'])
def sign_up():
    new_user = request.json
    print(new_user)
    connection = app.database.connect()
    try:
        result = connection.execute(text("""
        INSERT INTO `miniter`.`users` (
            `name`,
            `email`,
            `profile`,
            `hashed_password`
        ) VALUES (
            :name,
            :email,
            :profile,
            :hashed_password
        )
        """), new_user)
        new_user_id = result.lastrowid
    finally:
        connection.close()

    connection = app.database.connect()
    try:
        row = connection.execute(text("""
        SELECT
            `id`,
            `name`,
            `email`,
            `profile`
        FROM `miniter`.`users`
        WHERE `id` = :user_id;
        """), {'user_id': new_user_id}).fetchone()
    finally:
        connection.close()

    print(row)

    created_user = {
        'id': row['id'],
        'name': row['name'],
        'email': row['email'],
        'profile': row['profile']
    } if row else None

    print(created_user)

    return jsonify(created_user)

@app.route("/tweet", methods=['POST'])
def tweet():
    payload = request.json
    user_id = int(payload["id"])
    tweet = payload["tweet"]

    if user_id not in app.users:
        return "사용자가 존재하지 않습니다.", 400

    if len(tweet) > 300:
        return "트윗이 300자를 초과했습니다.", 400

    user_id = int(payload["id"])

    app.tweets.append({
        "user_id": user_id,
        "tweet": tweet
    })

    return "트윗 생성이 성공했습니다.", 200


@app.route("/follow", methods=['POST'])
def follow():
    payload = request.json
    user_id = int(payload['id'])
    user_id_to_follow = int(payload['follow'])

    if user_id not in app.users or user_id_to_follow not in app.users:
        return "사용자가 존재하지 않습니다.", 400

    user = app.users[user_id]
    user.setdefault('follow', set()).add(user_id_to_follow)

    return jsonify(user)


@app.route("/unfollow", methods=['POST'])
def unfollow():
    payload = request.json
    user_id = int(payload['id'])
    user_id_to_follow = int(payload['unfollow'])

    if user_id not in app.users or user_id_to_follow not in app.users:
        return "사용자가 존재하지 않습니다.", 400

    user = app.users[user_id]
    user.setdefault('follow', set()).discard(user_id_to_follow)

    return jsonify(user)


@app.route("/timeline/<int:user_id>", methods=["GET"])
def timeline(user_id):
    if user_id not in app.users:
        return "사용자가 존재하지 않습니다.", 400

    follow_list = app.users[user_id].get("follow", set())
    follow_list.add(user_id)
    timeline = [tweet for tweet in app.tweets if tweet['user_id'] in follow_list]

    return jsonify({
        "user_id": user_id,
        "timeline": timeline
    })