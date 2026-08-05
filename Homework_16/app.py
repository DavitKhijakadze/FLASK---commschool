from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/multiply/<int:a>/<int:b>/<int:c>/<int:d>", methods=["GET", "POST"])
def multiply(a, b, c, d):
    result = a * b * c * d

    return render_template("multiply.html", num1 = a, num2 = b, num3 = c, num4 = d, result = result)

@app.route("/info", methods=["GET", "POST"])
def get_info():
    user_data = {
        "name": "დავით",
        "lastname": "ხიჯაკაძე",
        "age": 30,
        "is_commschoool_student": True,
        "skills": ["HTML", "CSS", "Python", "Flask"],
        "location": {
            "city": "თბილისი",
            "country": "საქართველო"
        }
    }

    return jsonify(user_data)

@app.route("/greet/<username>", methods=["GET", "POST"])
def greet(username):
    return render_template("greet.html", name=username)

@app.errorhandler(404)
def page_not_found(e):
    html_content = """
    <style>
        .error-title {
            color: darkred;
            text-align: center;
            font-size: 28px;
            margin-top: 20%;
        }
    </style>
    <h1 class="error-title">თქვენ მოხვდით არარსებულ გვერდზე, გთხოვთ დაბრუნდეთ მთავარ გვერდზე!</h1>
    """
    return html_content, 404

if __name__ == "__main__":
    app.run(debug=True)