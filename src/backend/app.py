from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import func, select
from database import Click, db
import traceback

app = Flask(__name__)
app.total_clicks = 0
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/api/counts', methods=['GET', 'POST'])
@cross_origin()
@limiter.limit("5/second", override_defaults=False)
def main_endpoint():
    if request.method == 'GET':
        return jsonify({'clicks': app.total_clicks})
    elif request.method == 'POST':
        app.total_clicks += 1

        try:
            db.add(Click(app.total_clicks, request.headers.get('CF-Connecting-IP') or request.remote_addr))
            db.commit()
            return "", 204
        except:
            traceback.print_exc()
            return jsonify({'message': traceback.format_exc()}), 500


@app.teardown_appcontext
def shutdown_session(exception=None):
    db.remove()


if __name__ == "__main__":
    app.total_clicks = db.execute(
        select([func.count()]).select_from(Click.__table__)).scalar()
    app.run(debug=True)
