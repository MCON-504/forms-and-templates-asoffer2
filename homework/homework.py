from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# In-memory storage
students = []


@app.route("/")
def home():
    return redirect(url_for("add_student"))


# ---------------------------------
# TODO: IMPLEMENT THIS ROUTE
# ---------------------------------
@app.route("/add", methods=["GET", "POST"])
def add_student():
    error = None

    if request.method == "POST":
        name = request.form.get("name")
        grade = request.form.get("grade")

        # TODO:
        # 1. Validate name
        if name.strip() == "":
            error = "Name is empty"
        # 2. Validate grade is number
        else:
            try:
                grade = int(grade)
            except ValueError:
                error = "grade is not a number"
        # 3. Validate grade range 0–100
            else:
                if grade < 0 or grade > 100:
                    error = "grade is not between 0 and 100"
                else:
        # 4. Add to students list as dictionary
                    students.append({"name": name, "grade": grade})
        # 5. Redirect to /students
                    return redirect("/students")

    return render_template("add.html", error=error)


# ---------------------------------
# TODO: IMPLEMENT DISPLAY
# ---------------------------------
@app.route("/students")
def display_students():

    return render_template("students.html", students=students)


# ---------------------------------
# TODO: IMPLEMENT SUMMARY
# ---------------------------------
@app.route("/summary")
def summary():
    if len(students) == 0:
        error = "No students"
        return render_template("summary.html", error=error)
    # TODO:
    # Calculate:
    # - total students
    else:
        total_students = len(students)
        # - average grade
        count = 0
        grade_sum = 0
        highest_grade = None
        lowest_grade = None
        for student_dict in students:
            for key, value in student_dict.items():
                if key == "grade":
                    grade_sum += value
                    count += 1
                    if highest_grade is None or value > highest_grade:
                        highest_grade = value
                    if lowest_grade is None or value < lowest_grade:
                        lowest_grade = value
        average_grade = grade_sum/count


    # - highest grade
    # - lowest grade

    return render_template("summary.html", total_student=total_students,
                avg_grade=average_grade, high_grade=highest_grade, low_grade=lowest_grade)


if __name__ == "__main__":
    app.run(host="localhost", port=5001, debug=True)
