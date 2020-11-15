import functools, json
import psycopg2.extras

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from . import db

bp = Blueprint('index', __name__, url_prefix='/')


@bp.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@bp.route('/mapdata', methods=['GET'])
def mapdata():
    conn = db.get_db()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute(
        """
        SELECT ST_AsGeoJSON(t.*)
        FROM (SELECT * FROM tl_2019_us_county T WHERE T.statefp != '02' AND T.statefp != '09' AND T.statefp != '23' AND T.statefp != '33' AND T.statefp != '44' AND T.statefp != '50' AND T.statefp != '11')
        AS t(id, name, geom)

        UNION

        SELECT ST_AsGeoJSON(t.*)
        FROM (SELECT * FROM tl_2019_us_state T WHERE T.statefp = '02' OR T.statefp = '09' OR T.statefp = '23' OR T.statefp = '33' OR T.statefp = '44' OR T.statefp = '50' OR T.statefp = '11')
        AS t(id, name, geom);
        """
    )
    records = cursor.fetchall()
    return json.dumps(records)


@bp.route('/coviddata', methods=['GET'])
def coviddata():
    pass