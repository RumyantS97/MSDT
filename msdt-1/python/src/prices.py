import math

from flask import Flask
from flask import request
from datetime import datetime
from db import create_lift_pass_db_connection

app = Flask("lift-pass-pricing")

connection_options = {
    "host": 'localhost',
    "user": 'root',
    "database": 'lift_pass',
    "password": 'mysql'}

connection = None

@app.route("/prices", methods=['GET', 'PUT'])
def prices():
    res = {}
    global connection
    if connection is None:
        # if connection is not set
        connection = create_lift_pass_db_connection(connection_options)

    if request.method == 'PUT':
        lift_pass_cost = request.args["cost"]
        lift_pass_type = request.args["type"]
        cursor = connection.cursor()
        cursor.execute('INSERT INTO `base_price` (type, cost) VALUES (?, ?) ' +
            'ON DUPLICATE KEY UPDATE cost = ?', (lift_pass_type, lift_pass_cost, lift_pass_cost))
        return {}

    elif request.method == 'GET':
        cursor = connection.cursor()
        cursor.execute(f'SELECT cost FROM base_price '
                       + 'WHERE type = ? ', (request.args['type'],))

        row = cursor.fetchone()
        if row is None:
            # if no lift pass is found
            return {"error": "No lift pass found for this type."}
        result = {"cost": row[0]}

        if 'age' in request.args:
            age = request.args.get('age', type=int)
        else:
            age = None

        if age and age < 6:
            # free for children under 6
             res["cost"] = 0
        else:
            if "type" in request.args and request.args["type"] != "night":
                # apply non night pass reduction
                apply_reduction(res, request.args, result)
            else:
                # apply night pass reduction
                handle_night_pass(res, request.args, result)
    return res

def apply_reduction(res, args, result):
    """
    Apply the reduction to the cost of the lift pass
    The result is placed in the res variable
    """
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM holidays')
    is_holiday = check_holiday(cursor, args.get("date"))
    reduction = 0
    
    if not is_holiday and "date" in args and datetime.fromisoformat(args["date"]).weekday() == 0:
        # monday non holiday reduction
        reduction = 35
    
    age = args.get("age", type=int)
    if age < 15:
        res["cost"] = math.ceil(result["cost"] * 0.7)
    else:
        cost = result["cost"] * (1 - reduction / 100)
        if age > 64:
            cost *= 0.75
        res["cost"] = math.ceil(cost)


def check_holiday(cursor, date_str):
    """
    Check if the date is a holiday
    If date not provided, return False
    """
    if not date_str:
        return False
    date = datetime.fromisoformat(date_str)
    for row in cursor.fetchall():
        holiday = row[0]
        if date.year == holiday.year and date.month == holiday.month and holiday.day == date.day:
            return True
    return False


def handle_night_pass(res, args, result):
    """
    Handle the night pass.
    Places cost in the result variable if no reduction is applied
    Or applies a reduction and places the cost to the res
    """
    age = args.get("age", type=int)
    if age >= 6:
        if age > 64:
            res["cost"] = math.ceil(result["cost"] * 0.4)
        else:
            # if no reduction is applied
            res.update(result)
    else:
        res["cost"] = 0


if __name__ == "__main__":
    app.run(port=3005)
