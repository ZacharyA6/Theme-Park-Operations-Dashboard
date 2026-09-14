from flask import Flask, render_template, jsonify, request
import sqlite3

app = Flask(__name__)

# Open a connection to the SQLite database and 
# allow rows to be accessed by column name
def get_db_connection():
    conn = sqlite3.connect("park.db")
    conn.row_factory = sqlite3.Row
    return conn

# Create the rides table if it is the first time the app is run
def create_database():
    conn = get_db_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS rides (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            ride_type TEXT NOT NULL,
            wait_time INTEGER NOT NULL,
            capacity INTEGER NOT NULL,
            status TEXT NOT NULL
        )
    """)

    # Add starter rides if database is empty
    ride_count = conn.execute(
        "SELECT COUNT(*) FROM rides"
    ).fetchone()[0]

    if ride_count == 0:
        rides = [
            ("Minecart Mayhem", "Roller Coaster", 45, 24, "Operating"),
            ("We're Still Falling!", "Water Ride", 30, 12, "Operating"),
            ("Beyond the Little Door", "Dark Ride", 20, 18, "Operating"),
            ("Wagon Wheel", "Ferris Wheel", 10, 32, "Operating"),
            ("Lightspeed Getaway", "Thrill Ride", 0, 16, "Closed"),
            ("The Magic Wardrobe", "Family Ride", 25, 20, "Delayed")
        ]

        conn.executemany("""
            INSERT INTO rides
            (name, ride_type, wait_time, capacity, status)
            VALUES (?, ?, ?, ?, ?)
        """, rides)

    conn.commit()
    conn.close()


@app.route("/")
def home():
    return render_template("index.html")

# Return ride data as JSON for the frontend dashboard
@app.route("/api/rides")
def get_rides():
    conn = get_db_connection()

    rides = conn.execute(
        "SELECT * FROM rides"
    ).fetchall()

    conn.close()

    return jsonify([
        dict(ride) for ride in rides
    ])

@app.route("/api/rides/<int:rides_id>", methods=["PUT"])
def update_ride(rides_id):
    data = request.get_json()

    wait_time = data.get("wait_time")
    capacity = data.get("capacity")
    status = data.get("status")

    # User input error handling
    if wait_time is None or capacity is None or status is None:
        return jsonify({
            "error": "Missing required field(s)"
        }), 400

    if type(wait_time) is not int:
        return jsonify({
            "error" : "Wait time must be an integer"
        }), 400

    if type(capacity) is not int:
            return jsonify({
                "error" : "Capacity must be an integer"
            }), 400

    if wait_time < 0 or wait_time > 180:
        return jsonify({
            "error": "Wait time must be between 0 and 180"
        }), 400

    if capacity < 1 or capacity > 100:
        return jsonify({
            "error": "Capacity must be between 1 and 100"
        }), 400

    # Restrict status to supported values
    valid_statuses = [
        "Operating",
        "Delayed",
        "Closed"
    ]

    if status not in valid_statuses:
        return jsonify({
            "error": "Invalid ride status"
        }), 400

    try:
        conn = get_db_connection()

        cursor = conn.execute("""
            UPDATE rides

                SET wait_time = ?,
                    capacity = ?,
                    status = ?

                WHERE id = ?
            """, (
                data["wait_time"],
                data["capacity"],
                data["status"],
                rides_id
            ))

        # Return 404 if no ride exists with given ID
        if cursor.rowcount == 0:
            conn.close()

            return jsonify({
                "error": "Ride not found"
            }), 404

        conn.commit()
    except sqlite3.Error as error:
        print(error)

        return jsonify({
            "error" : "Database error"
        }), 500

    finally:
        if conn:
            conn.close()

    return jsonify({
        "message" : "Ride updated successfully"
    })

if __name__ == "__main__":
    create_database()
    app.run(debug=True)