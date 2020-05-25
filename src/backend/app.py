from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_limiter import Limiter
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import func, select
from database import Click, db
import traceback

app = Flask(__name__)
app.total_clicks = 0
CORS(app)
limiter = Limiter(app, key_func=lambda: request.remote_addr,
                  default_limits=["200 per day", "50 per hour"])


@app.route('/api/counts', methods=['GET', 'POST'])
@limiter.limit("5/second", override_defaults=False)
def main_endpoint():
    if request.method == 'GET':
        return jsonify({'clicks': app.total_clicks})
    elif request.method == 'POST':
        app.total_clicks += 1
        db.add(Click(app.total_clicks, request.remote_addr))
        db.commit()
        return "", 204
    else:
        return "", 405


@app.before_request
def before_request():
    request.remote_addr = request.headers.get(
        "CF-Connecting-IP") or request.headers.get("X-Forwarded-For") or request.remote_addr


@app.errorhandler(Exception)
def handle_500():
    traceback.print_exc()
    return jsonify({"message": traceback.format_exc()}), 500


@app.errorhandler(404)
def handle_404(error):
    return jsonify({"message": "The requested route was not found"}), 404


@app.errorhandler(405)
def handle_405(error):
    return jsonify({"message": "Method not allowed"}), 405


@app.teardown_appcontext
def shutdown_session(exception=None):
    db.remove()


if __name__ == "__main__":
    app.total_clicks = db.execute(
        select([func.count()]).select_from(Click.__table__)).scalar()
    app.run(debug=True)
