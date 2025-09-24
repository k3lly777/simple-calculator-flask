from flask import Flask, render_template
import os

app = Flask(__name__)

# Route for the homepage
@app.route("/")
def index():
    return render_template("index.html")

# Run the app
if __name__ == "__main__":
    # Get the port from environment variable (for Render) or default to 5000 (local)
    port = int(os.environ.get("PORT", 5000))
    # host="0.0.0.0" allows access from any IP (required for Render)
    app.run(host="0.0.0.0", port=port, debug=True)
