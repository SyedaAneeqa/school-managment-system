
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash


def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",  # Change if you set a password
        password="",  # Keep empty if using default XAMPP settings
        database="school management"
    )


app = Flask(__name__)
app.secret_key = "your_secret_key"

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://root:@localhost/school management"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

# User Model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(200), nullable=False)  
    role = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), default="pending")


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        role = request.form["role"]
        username = request.form["username"]

        # Check if the email already exists
        if User.query.filter_by(email=email).first():
            flash("Email already exists!", "danger")
            return redirect(url_for("signup"))

        # Set status: auto-approve admin, pending for others
       
        status = "pending"

        new_user = User(
            username=username,
            email=email,
            password=password,  # Consider hashing in future
            role=role,
            status=status
        )
        db.session.add(new_user)
        db.session.commit()

        if status == "approved":
            flash("Signup successful! You can now log in.", "success")
        else:
            flash("Signup successful! Wait for admin approval.", "info")

        return redirect(url_for("login"))

    return render_template("signup.html")
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        role = request.form["role"]

        user = User.query.filter_by(email=email).first()

        if user:
            # Allow login only if user is approved or is an admin
            if user.status != "approved":
                flash("Your account is pending approval by admin.", "warning")
                return redirect(url_for("login"))

            if user.password == password and user.role.lower() == role.lower():
                login_user(user)
                session["role"] = user.role
                session["username"] = user.username
                session["student_id"] = user.id
                flash("Login successful!", "success")

                if user.role.lower() == "admin":
                    return redirect(url_for("admindashboard"))
                elif user.role.lower() == "student":
                    return redirect(url_for("studentdashboard"))
                elif user.role.lower() == "teacher":
                    return redirect(url_for("teacherdashboard"))
            else:
                flash("Invalid password or role!", "danger")
        else:
            flash("Invalid email!", "danger")

    return render_template("login.html")



@app.route("/approve_user", methods=["GET", "POST"])
def approve_users():
    if session.get("role") != "Admin":
        return redirect("/")

    pending_users = User.query.filter_by(status="pending").all()

    if request.method == "POST":
        user_id = request.form.get("user_id")
        user = User.query.get(user_id)
        if user:
            user.status = "approved"
            db.session.commit()
            flash(f"User '{user.username}' approved!", "success")
        return redirect(url_for("approve_users"))

    return render_template("approve_users.html", pending_users=pending_users)


@app.route("/admindashboard")
def admindashboard():
    if "role" not in session or session["role"] != "Admin":
        return redirect("/")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Count total students
    cursor.execute("SELECT COUNT(*) AS total_students FROM students")
    total_students = cursor.fetchone()["total_students"]

    # Count total teachers
    cursor.execute("SELECT COUNT(*) AS total_teachers FROM teachers")
    total_teachers = cursor.fetchone()["total_teachers"]

    conn.close()

    return render_template("admindashboard.html", total_students=total_students, total_teachers=total_teachers)


 

@app.route("/admin_teacher", methods=["GET", "POST"])
def admin_teacher():
    # Restrict access to Admin role only
    if "role" not in session or session["role"].lower() != "admin":
        return redirect("/")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]
        username = request.form["username"]
        mobile = request.form["mobile"]
        salary = request.form["salary"]
        classno = request.form["classno"]

        query = """
            INSERT INTO teachers (firstname, lastname, username, mobile, salary, classno)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (firstname, lastname, username, mobile, salary, classno))
        conn.commit()

        return redirect("/admin_teacher")  # Refresh page after inserting

    # Fetch and display all teachers
    cursor.execute("SELECT * FROM teachers")
    teachers = cursor.fetchall()

    conn.close()
    return render_template("admin_teacher.html", teachers=teachers)

@app.route("/delete-teacher/<username>")
def delete_teacher(username):
    if "role" not in session or session["role"] != "Admin":
        return redirect("/")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM teachers WHERE username = %s", (username,))
    conn.commit()
    conn.close()

    return redirect("/admin_teacher")
@app.route("/admin_student", methods=["GET", "POST"])
def admin_student():
    if "role" not in session or session["role"] != "Admin":
        return redirect("/")  # Restrict access to admin only

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]
        rollnumber = request.form["rollnumber"]
        classno = request.form["classno"]
        batch = request.form["batch"]
        guardianname = request.form["guardianname"]
        mobile = request.form["mobile"]

        query = "INSERT INTO students (firstname, lastname, rollnumber, classno,batch, guardianname, mobile) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (firstname, lastname, rollnumber, classno,batch, guardianname, mobile))
        conn.commit()

        return redirect("/admin_student")  # Refresh page

    # Fetch all students
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    conn.close()
    return render_template("admin_student.html", students=students)

@app.route("/delete-student/<rollnumber>/<classno>")
def delete_student(rollnumber, classno):
    if "role" not in session or session["role"] != "Admin":
        return redirect("/")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE rollnumber = %s AND classno = %s", (rollnumber, classno))
    conn.commit()
    conn.close()

    return redirect("/admin_student")
@app.route("/admin_notice", methods=["GET", "POST"])
def admin_notice():
    if "role" not in session or session["role"] != "Admin":
        return redirect("/")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":
        notice_text = request.form["notice_text"]
        cursor.execute("INSERT INTO notices (notice_text) VALUES (%s)", (notice_text,))
        conn.commit()

    # Fetch all notices (latest first)
    cursor.execute("SELECT * FROM notices ORDER BY date_posted DESC")
    notices = cursor.fetchall()

    conn.close()

    return render_template("admin_notice.html", notices=notices)

# Route to delete a notice
@app.route("/delete_notice/<int:notice_id>", methods=["POST"])
def delete_notice(notice_id):
    if "role" not in session or session["role"] != "Admin":
        return redirect("/")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM notices WHERE id = %s", (notice_id,))
    conn.commit()
    conn.close()

    return redirect(url_for("admin_notice"))


@app.route("/studentdashboard", methods=["GET", "POST"])
def studentdashboard():
    # Ensure the user is logged in as a student
    if "role" not in session or session["role"] != "Student":
        return redirect("/")  # Redirect to login if not logged in
    
    return render_template("studentdashboard.html")


@app.route("/view_grades", methods=["GET", "POST"])
def view_grades():
    grades = []  # Empty by default
    if request.method == "POST":
        student_id = request.form.get("student_id")
        
        if student_id:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT subject, grade
                FROM grades
                WHERE student_id = %s
            """, (student_id,))
            grades = cursor.fetchall()
            conn.close()
    
    return render_template("view_grades.html", grades=grades)



@app.route("/select_courses")
def select_courses():
    # Ensure the user is logged in as a student
    if "role" not in session or session["role"] != "Student":
        return redirect("/")  # Redirect to login if not logged in
    
    student_id = session["student_id"]
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Get available courses for the student
    cursor.execute("""
    SELECT c.course_id, c.course_name, c.class, c.type
    FROM course c
    WHERE c.course_id NOT IN (
        SELECT course_id
        FROM student_courses
        WHERE student_id = %s
    )
    """, (student_id,))
    available_courses = cursor.fetchall()
    conn.close()
    return render_template("select_courses.html", available_courses=available_courses)


@app.route("/submit_course_selection", methods=["POST"])
def submit_course_selection():
    # No longer require the student to be logged in, so we remove the session check
    # (You can still keep user authentication, but not specifically the student ID)
    
    student_id = request.form.get("student_id")  # You can pass the student_id from the form if needed
    course_id = request.form.get("course_id")
    
    if student_id and course_id:  # Ensure both student_id and course_id are provided
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Insert the selected course into the student_courses table
        cursor.execute("""
            INSERT INTO student_courses (student_id, course_id)
            VALUES (%s, %s)
        """, (student_id, course_id))
        conn.commit()
        conn.close()
        
        message = "Course selected successfully!"
    else:
        message = "Please select a valid course."
    
    return render_template("select_courses.html", message=message)
@app.route("/view_attendance", methods=["GET", "POST"])
def view_attendance():
    attendance = None  # Default: no data
    
    if request.method == "POST":
        student_id = request.form.get("student_id")
        
        if student_id:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT date, status
                FROM attendance
                WHERE student_id = %s
                ORDER BY date DESC
            """, (student_id,))
            attendance = cursor.fetchall()
            conn.close()
    
    return render_template("view_attendance.html", attendance=attendance)






@app.route("/teacherdashboard")
def teacherdashboard():
    if "role" not in session or session["role"] != "Teacher":
        return redirect("/")
    return render_template("teacherdashboard.html")

@app.route("/grade_management", methods=["GET", "POST"])
def grade_management():
    if "role" not in session or session["role"] != "Teacher":
        return redirect("/")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Get class filter from URL (GET request)
    selected_class = request.args.get("classno")

    # Handle POST request to add a grade
    if request.method == "POST":
        student_id = request.form["student"]
        subject = request.form["subject"]
        grade = request.form["grade"]

        query = "INSERT INTO grades (student_id, subject, grade) VALUES (%s, %s, %s)"
        cursor.execute(query, (student_id, subject, grade))
        conn.commit()
        flash("Grade added successfully!", "success")

    # Fetch grades based on selected class
    if selected_class:
        cursor.execute("""
            SELECT g.id, CONCAT(s.firstname, ' ', s.lastname) AS student_name, s.classno, g.subject, g.grade
            FROM grades g
            JOIN students s ON g.student_id = s.id
            WHERE s.classno = %s
        """, (selected_class,))
    else:
        cursor.execute("""
            SELECT g.id, CONCAT(s.firstname, ' ', s.lastname) AS student_name, s.classno, g.subject, g.grade
            FROM grades g
            JOIN students s ON g.student_id = s.id
        """)
    grades = cursor.fetchall()

    # Fetch students (filtered by class if selected)
    if selected_class:
        cursor.execute("SELECT * FROM students WHERE classno = %s", (selected_class,))
    else:
        cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    # Get distinct class numbers
    cursor.execute("SELECT DISTINCT classno FROM students")
    classes = [row["classno"] for row in cursor.fetchall()]

    conn.close()
    return render_template("grade_management.html",
                           grades=grades,
                           students=students,
                           selected_class=selected_class,
                           classes=classes)


from datetime import date

@app.route("/attendance_management", methods=["GET", "POST"])
def attendance_management():
    if "role" not in session or session["role"] != "Teacher":
        return redirect("/")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":
        date_selected = request.form.get("date")
        classno = request.form.get("classno")

        if not classno:
            return redirect(url_for("attendance_management"))

        # Get students from the selected class
        cursor.execute("SELECT id FROM students WHERE classno = %s", (classno,))
        student_ids = [s["id"] for s in cursor.fetchall()]

        # Save attendance
        for student_id in student_ids:
            status = request.form.get(f"attendance_{student_id}")
            if status:
                cursor.execute("""
                    INSERT INTO attendance (student_id, date, status, classno)
                    VALUES (%s, %s, %s, %s)
                """, (student_id, date_selected, status, classno))

        conn.commit()
        return redirect(url_for('attendance_management', classno=classno))

    # GET request
    selected_class = request.args.get("classno")
    students = []
    attendance_records = []

    if selected_class:
        # Fetch students from the selected class
        cursor.execute("SELECT * FROM students WHERE classno = %s", (selected_class,))
        students = cursor.fetchall()

        # Fetch today's attendance for selected class
        cursor.execute("""
            SELECT CONCAT(s.firstname, ' ', s.lastname) AS student_name, a.status
            FROM attendance a
            JOIN students s ON a.student_id = s.id
            WHERE a.date = CURDATE() AND a.classno = %s
        """, (selected_class,))
        attendance_records = cursor.fetchall()

    # Get all distinct classes
    cursor.execute("SELECT DISTINCT classno FROM students")
    classes = [row["classno"] for row in cursor.fetchall()]

    conn.close()

    return render_template(
        "attendance_management.html",
        students=students,
        classes=classes,
        selected_class=selected_class,
        attendance_records=attendance_records,
        current_date=date.today().isoformat()
    )
@app.route('/chatbot', methods=['GET', 'POST'])
def chatbot():
    response = None

    if request.method == 'POST':
        user_input = request.form['user_input'].lower()

        # Simple replies to common greetings
        if 'hello' in user_input or 'hi' in user_input:
            response = "Hello! How can I assist you today?"
        elif 'how are you' in user_input:
            response = "I'm just a bot, but I'm here to help you!"

        # Student dashboard questions
        elif 'student dashboard' in user_input:
            response = "The student dashboard includes options like View Grades, View Attendance, and Select Courses."
        
        elif 'view grades' in user_input:
            response = "You can view your grades from the 'View Grades' section. Just click on 'View Grades' from the dashboard."
        
        elif 'select course' in user_input or 'course registration' in user_input:
            response = "You can select courses from the 'Select Courses' section. Navigate there from the student dashboard."

        elif 'view attendance' in user_input:
            response = "You can view your attendance from the 'View Attendance' section. Click 'View Attendance' to see your attendance details."

        # Teacher dashboard questions
        elif 'teacher dashboard' in user_input:
            response = "The teacher dashboard includes options like Grade Management, Attendance Tracking, and Chatbot."
        
        elif 'grade management' in user_input:
            response = "You can manage student grades from the 'Grade Management' section in the teacher dashboard."

        elif 'view attendance' in user_input:
            response = "You can view attendance for students from the 'view attendance' section on student dashboard."
        elif 'mark attendance' in user_input:
            response = "You can mark attendance for students from the 'Attendance Trcking' section on teacher dashboard."
        
        # Admin dashboard questions
        elif 'admin dashboard' in user_input:
            response = "The admin dashboard includes options to manage Teachers, Students, Notices, and more. Select any option from the dashboard."
        
        elif 'manage teachers' in user_input:
            response = "As an admin, you can manage teachers from the 'Teachers' section in the admin dashboard."

        elif 'manage students' in user_input:
            response = "You can manage students, including adding and editing their details, from the 'Students' section in the admin dashboard."
        
        elif 'manage notices' in user_input:
            response = "You can manage notices for students and teachers from the 'Notices' section in the admin dashboard."

        # Common replies
        elif 'logout' in user_input:
            response = "You can logout by clicking the 'Logout' button on top."
        
        elif 'help' in user_input:
            response = "You can ask me about grades, attendance, courses, dashboard features, or admin tasks."

        elif 'chatbot' in user_input:
            response = "The chatbot helps you navigate through different sections. Feel free to ask about the dashboard, grades, attendance, and more!"

        elif 'dashboard' in user_input:
            response = "The dashboard gives you access to your important options based on your role."

        # More generic questions that might be useful for all dashboards
        elif 'how to' in user_input or 'where to' in user_input:
            response = "You can navigate to the relevant section in the dashboard: 'View Grades', 'Select Courses', 'Mark Attendance', 'Manage Teachers', 'Manage Students', etc."

        else:
            response = "I'm sorry, I didn't understand that. Please try asking about grades, attendance, courses, or help."

    return render_template('chatbot.html', response=response)
@app.route("/logout")
def logout():
    logout_user()
    session.pop("role", None)  # Remove role from session
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
