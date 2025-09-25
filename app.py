
# --- Imports ---

from flask import Flask, render_template # Imports Flask (which is the main class used to create the web app) and render_template (which makes it possible to return HTML file from "templates/")

# --- App ---

app = Flask(__name__, static_folder = "static", template_folder = "templates") # Creates Flask app object and specifies where it lives and where it will look for files

@app.route("/") # Route decorator which states that the code below should run when a user goes to "/" (i.e visits the homepage)

def index():

    """
    Returns the file "templates/index.html" to the browser.

    Arguments:
        None

    Returns:
        "render_template("index.html")": 

    """
    return render_template("index.html")

if __name__ == "__main__": # If app.py is run directly (i.e not imported as a module in another file):
    app.run(debug = True)