
# --- Imports ---
import os
from flask import Flask, render_template, jsonify # Imports Flask (which is the main class used to create the web app) and render_template (which makes it possible to return HTML file from "templates/")
from datetime import datetime
# --- App ---

app = Flask(__name__, static_folder = "static", template_folder = "templates") # Creates Flask app object and specifies where it lives and where it will look for files

VISITS_FILE = "visits.txt"

@app.route("/") # Route decorator which states that the code below should run when a user goes to "/" (i.e visits the homepage)

def index():

    """
    Records a visit and returns the homepage.

    Arguments:
        None

    Returns:
        Rendered HTML of "index.html" template.
        Also logs the visit timestamp to VISITS_FILE.

    """
     # Records the visit
    timestamp = datetime.now().isoformat()
    with open(VISITS_FILE, "a") as f:
        f.write(timestamp + "\n") 
    
    return render_template("index.html")

@app.route("/visits")
def visits_route():
    """
    Returns all visits as JSON.
    """
    if not os.path.exists(VISITS_FILE):
        return jsonify([])
    with open(VISITS_FILE, "r") as f:
        lines = f.readlines()
    visits = [line.strip() for line in lines]
    return jsonify(visits)

if __name__ == "__main__": # If app.py is run directly (i.e not imported as a module in another file):
    app.run(debug = True)