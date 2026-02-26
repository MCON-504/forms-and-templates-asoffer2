import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# -------------------------------------------------
# Create templates automatically (for demo ease)
# -------------------------------------------------

def create_templates():
    os.makedirs("demo/templates", exist_ok=True)

    base_template = """<!DOCTYPE html>
<html>
<head>
    <title>Jinja2 Demo</title>
    <style>
        body { font-family: Arial; margin: 40px; }
        nav a { margin-right: 15px; }
        .error { color: red; }
        .box { padding: 10px; border: 1px solid #ccc; margin: 10px 0; }
    </style>
</head>
<body>

<nav>
    <a href="{{ url_for('home') }}">Home</a>
    <a href="{{ url_for('conditionals') }}">Conditionals</a>
    <a href="{{ url_for('loops') }}">Loops</a>
    <a href="{{ url_for('filters_demo') }}">Filters</a>
    <a href="{{ url_for('form_demo') }}">Form</a>
</nav>

<hr>

{% block content %}{% endblock %}

<hr>
<footer>
    Current time: {{ now }}
</footer>

</body>
</html>
"""

    home_template = """{% extends "base.html" %}
{% block content %}
<h1>Welcome {{ name }}!</h1>
<p>This page demonstrates:</p>
<ul>
    <li>Variable interpolation</li>
    <li>Template inheritance</li>
    <li>Context variables</li>
</ul>
{% endblock %}
"""

    conditional_template = """{% extends "base.html" %}
{% block content %}
<h2>Conditionals Demo</h2>

{% if score >= 90 %}
    <div class="box">Grade: A</div>
{% elif score >= 70 %}
    <div class="box">Grade: B</div>
{% else %}
    <div class="box">Keep practicing!</div>
{% endif %}

{% endblock %}
"""

    loops_template = """{% extends "base.html" %}
{% block content %}
<h2>Loops Demo</h2>

<ul>
{% for student in students %}
    <li>{{ loop.index }}. {{ student }}</li>
{% endfor %}
</ul>

<p>Total students: {{ students|length }}</p>

{% endblock %}
"""

    filters_template = """{% extends "base.html" %}
{% block content %}
<h2>Filters Demo</h2>

<p>Original name: {{ name }}</p>
<p>Uppercase: {{ name|upper }}</p>
<p>Lowercase: {{ name|lower }}</p>
<p>Title case: {{ name|title }}</p>

<p>Formatted number: {{ number|round(2) }}</p>

{% endblock %}
"""

    form_template = """{% extends "base.html" %}
{% block content %}
<h2>Form Demo</h2>

{% if error %}
    <p class="error">{{ error }}</p>
{% endif %}

<form method="POST">
    <label>Name:</label>
    <input type="text" name="username">
    <button type="submit">Submit</button>
</form>

{% if submitted_name %}
    <div class="box">
        Hello {{ submitted_name }}!
    </div>
{% endif %}

{% endblock %}
"""

    templates = {
        "base.html": base_template,
        "home.html": home_template,
        "conditionals.html": conditional_template,
        "loops.html": loops_template,
        "filters.html": filters_template,
        "form.html": form_template
    }

    for filename, content in templates.items():
        with open(os.path.join("demo/templates", filename), "w", encoding="utf-8") as f:
            f.write(content)


# Create templates before first request
create_templates()


# -------------------------------------------------
# Routes
# -------------------------------------------------

@app.context_processor
def inject_now():
    return {"now": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}


@app.route("/")
def home():
    return render_template("home.html", name="Guest")


@app.route("/conditionals")
def conditionals():
    return render_template("conditionals.html", score=85)


@app.route("/loops")
def loops():
    students = ["Alice", "Bob", "Charlie", "Diana"]
    return render_template("loops.html", students=students)


@app.route("/filters")
def filters_demo():
    return render_template("filters.html", name="flask jinja demo", number=3.1415926)


@app.route("/form", methods=["GET", "POST"])
def form_demo():
    error = None
    submitted_name = None

    if request.method == "POST":
        submitted_name = request.form.get("username")

        if not submitted_name:
            error = "Name is required."

    return render_template(
        "form.html",
        error=error,
        submitted_name=submitted_name
    )


# -------------------------------------------------
# Run App
# -------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=5002)
