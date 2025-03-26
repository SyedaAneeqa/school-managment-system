# from flask import Flask, render_template, request, redirect, url_for, flash
# from flask_sqlalchemy import SQLAlchemy
# from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
# from werkzeug.security import generate_password_hash, check_password_hash

# app = Flask(__name__)
# app.secret_key = "your_secret_key"  # Needed for flash messages

# # ✅ Corrected MySQL Database URI (XAMPP)
# app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://root:@localhost/school management"
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db = SQLAlchemy(app)
# login_manager = LoginManager(app)
# login_manager.login_view = "login"  # Redirects unauthorized users to login page

# # ✅ User Model
# class User(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     username = db.Column(db.String(255), nullable=False)
#     email = db.Column(db.String(255), unique=True, nullable=False)
#     password = db.Column(db.String(255), nullable=False)
#     role = db.Column(db.String(50), nullable=False)

# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))

# @app.route("/")
# def home():
#     return render_template("index.html")

# # ✅ Signup Route (Fixes)
# @app.route("/signup", methods=["GET", "POST"])
# def signup():
#     if request.method == "POST":
#         username = request.form["username"]
#         email = request.form["email"]
#         password = request.form["password"]
#         role = request.form["role"]

#         # Check if email already exists
#         if User.query.filter_by(email=email).first():
#             flash("Email already exists! Try logging in.", "danger")
#             return redirect(url_for("signup"))

#         # ✅ Fixed Password Hashing
#         hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

#         # Add user to database
#         new_user = User(username=username, email=email, password=hashed_password, role=role)
#         db.session.add(new_user)
#         db.session.commit()

#         flash("Signup successful! You can now login.", "success")
#         return redirect(url_for("login"))

#     return render_template("signup.html")

# # ✅ Login Route (Fixed Debugging)

# @app.route("/login", methods=["GET", "POST"])
# def login():
#     if request.method == "POST":
#         email = request.form["email"]
#         password = request.form["password"]
#         role = request.form["role"]

#         user = User.query.filter_by(email=email).first()

#         if user:
#             print(f"DEBUG: Stored Role: '{user.role}', Entered Role: '{role}'")
#             print(f"DEBUG: Stored Password Hash: '{user.password}', Entered Password: '{password}'")
#             print(f"DEBUG: Password Match: {check_password_hash(user.password, password)}")

#             # ✅ Check role & verify password
#             if user.role.strip().lower() == role.strip().lower() and check_password_hash(user.password, password):
#                 login_user(user)
#                 flash("Login successful!", "success")

#                 # Redirect user based on role
#                 if user.role == "Admin":
#                     return redirect(url_for("admindashboard"))
#                 elif user.role == "Student":
#                     return redirect(url_for("studentdashboard"))
#                 elif user.role == "Teacher":
#                     return redirect(url_for("teacherdashboard"))
#             else:
#                 flash("Invalid password or role!", "danger")
#         else:
#             flash("Invalid email!", "danger")

#     return render_template("login.html")

# # ✅ Logout Route
# @app.route("/logout")
# @login_required
# def logout():
#     logout_user()
#     flash("You have been logged out.", "info")
#     return redirect(url_for("login"))

# # ✅ Admin Dashboard
# @app.route("/admindashboard")  # ✅ Fixed route name (Flask is case-sensitive)
# @login_required
# def admindashboard():
#     if current_user.role.lower() != "admin":
#         flash("Access Denied!", "danger")
#         return redirect(url_for("login"))
#     return render_template("admindashboard.html")

# # ✅ Student Dashboard
# @app.route("/studentdashboard")  # ✅ Fixed route name
# @login_required
# def studentdashboard():
#     if current_user.role.lower() != "student":
#         flash("Access Denied!", "danger")
#         return redirect(url_for("login"))
#     return render_template("studentdashboard.html")

# # ✅ Teacher Dashboard
# @app.route("/teacherdashboard")  # ✅ Fixed route name
# @login_required
# def teacherdashboard():
#     if current_user.role.lower() != "teacher":
#         flash("Access Denied!", "danger")
#         return redirect(url_for("login"))
#     return render_template("teacherdashboard.html")

# # ✅ Run Flask App
# if __name__ == "__main__":
#     with app.app_context():
#         db.create_all()  # Creates tables if they don't exist
#     app.run(debug=True)


# from flask import Flask, render_template, request, redirect, url_for, flash, session
# from flask_sqlalchemy import SQLAlchemy
# from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user
# from werkzeug.security import generate_password_hash, check_password_hash

# app = Flask(__name__)
# app.secret_key = "your_secret_key"
# app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://root:@localhost/school management"

# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# db = SQLAlchemy(app)
# login_manager = LoginManager(app)
# login_manager.login_view = "login"

# # User Model
# class User(UserMixin, db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(150), unique=True, nullable=False)
#     password = db.Column(db.String(200), nullable=False)
#     role = db.Column(db.String(20), nullable=False)

# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))

# # Route: Home
# @app.route("/")
# def home():
#     return render_template("index.html")

# # Route: Signup
# @app.route("/signup", methods=["GET", "POST"])
# def signup():
#     if request.method == "POST":
#         email = request.form["email"]
#         password = request.form["password"]
#         role = request.form["role"]

#         hashed_password = generate_password_hash(password, method="pbkdf2:sha256")  # Hash password before storing

#         if User.query.filter_by(email=email).first():
#             flash("Email already exists!", "danger")
#             return redirect(url_for("signup"))

#         new_user = User(email=email, password=hashed_password, role=role)
#         db.session.add(new_user)
#         db.session.commit()

#         flash("Signup successful! Please log in.", "success")
#         return redirect(url_for("login"))

#     return render_template("signup.html")

# # Route: Login
# @app.route("/login", methods=["GET", "POST"])
# def login():
#     if request.method == "POST":
#         email = request.form["email"]
#         password = request.form["password"]
#         role = request.form["role"]

#         user = User.query.filter_by(email=email).first()

#         if user:
#             print(f"DEBUG: Stored Role: '{user.role}', Entered Role: '{role}'")
#             print(f"DEBUG: Stored Password Hash: '{user.password}', Entered Password: '{password}'")
#             print(f"DEBUG: Password Check: {check_password_hash(user.password, password)}")

#             if user.role == role and check_password_hash(user.password, password):
#                 login_user(user)
#                 session["role"] = user.role  # Store role in session
#                 flash("Login successful!", "success")

#                 # Redirect user based on role
#                 if user.role == "Admin":
#                     return redirect(url_for("admindashboard"))
#                 elif user.role == "Student":
#                     return redirect(url_for("studentdashboard"))
#                 elif user.role == "Teacher":
#                     return redirect(url_for("teacherdashboard"))
#             else:
#                 flash("Invalid password or role!", "danger")
#         else:
#             flash("Invalid email!", "danger")

#     return render_template("login.html")

# # Route: Admin Dashboard
# @app.route("/admin_dashboard")
# def admindashboard():
#     if "role" in session and session["role"] == "Admin":
#         return "Welcome to the Admin Dashboard!"
#     return redirect(url_for("login"))

# # Route: Student Dashboard
# @app.route("/student_dashboard")
# def studentdashboard():
#     if "role" in session and session["role"] == "Student":
#         return "Welcome to the Student Dashboard!"
#     return redirect(url_for("login"))

# # Route: Teacher Dashboard
# @app.route("/teacher_dashboard")
# def teacherdashboard():
#     if "role" in session and session["role"] == "Teacher":
#         return "Welcome to the Teacher Dashboard!"
#     return redirect(url_for("login"))

# # Route: Logout
# @app.route("/logout")
# def logout():
#     logout_user()
#     session.pop("role", None)  # Remove role from session
#     flash("You have been logged out.", "info")
#     return redirect(url_for("login"))

# # Run the Flask App
# if __name__ == "__main__":
#     with app.app_context():
#         db.create_all()
#     app.run(debug=True)




from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user
import mysql.connector

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
    password = db.Column(db.String(200), nullable=False)  # Store plain text password
    role = db.Column(db.String(20), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
def home():
    return render_template("index.html")

# Signup Route
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]  # Save as plain text
        role = request.form["role"]
        username = request.form["username"]

        if User.query.filter_by(email=email).first():
            flash("Email already exists!", "danger")
            return redirect(url_for("signup"))

        new_user = User(username=username, email=email, password=password, role=role)
        db.session.add(new_user)
        db.session.commit()

        flash("Signup successful! Please log in.", "success")
        return redirect(url_for("login"))

    return render_template("signup.html")

# Login Route
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        role = request.form["role"]

        user = User.query.filter_by(email=email).first()

        if user:
            print(f"DEBUG: Stored Password: '{user.password}', Entered Password: '{password}'")

            if user.password == password and user.role.lower() == role.lower():
                login_user(user)
                session["role"] = user.role  # Store role in session
                session["username"] = user.username
                flash("Login successful!", "success")

                # Redirect user based on role
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


    # render_template("admindashboard.html")
@app.route("/admin_teacher", methods=["GET", "POST"])
def admin_teacher():
    if "role" not in session or session["role"] != "Admin":
        return redirect("/")  # Restrict access to admin only

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]
        username = request.form["username"]
        password = request.form["password"]
        mobile = request.form["mobile"]
        salary = request.form["salary"]
        classno = request.form["classno"]

        query = "INSERT INTO teachers (firstname, lastname, username, password, mobile, salary, classno) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (firstname, lastname, username, password, mobile, salary, classno))
        conn.commit()

        return redirect("/admin_teacher")  # Refresh page

    # Fetch all teachers
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
        guardianname = request.form["guardianname"]
        mobile = request.form["mobile"]

        query = "INSERT INTO students (firstname, lastname, rollnumber, classno, guardianname, mobile) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (firstname, lastname, rollnumber, classno, guardianname, mobile))
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

@app.route("/admin_attendance")
def admin_attendance():
    if "role" not in session or session["role"] != "Admin":
        return redirect("/")
    
    students = session.get("students", [])  # Retrieve students from session
    return render_template("admin_attendance.html", students=students)

@app.route("/studentDashboard")
def studentDashboard():
    if "role" not in session or session["role"] != "Student":
        return redirect("/")
    return "<h1>Welcome Student!</h1> <p>This is your dashboard.</p>"

@app.route("/teacherDashboard")
def teacherDashboard():
    if "role" not in session or session["role"] != "Teacher":
        return redirect("/")
    return "<h1>Welcome Teacher!</h1> <p>This is your dashboard.</p>"

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
