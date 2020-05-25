from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import func, select
from database import Click, db
import traceback

app = Flask(__name__)
app.total_clicks = 0
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/api/counts', methods=['GET', 'POST'])
@cross_origin()
def main_endpoint():
    if request.method == 'GET':
        return jsonify({'clicks': app.total_clicks})
    elif request.method == 'POST':
        app.total_clicks += 1

        try:
            db.add(Click(app.total_clicks, request.remote_addr))
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
