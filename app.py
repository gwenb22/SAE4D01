from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def scan():
    return render_template("scan.html")

if __name__ == "__main__":
    app.run(debug=True)
