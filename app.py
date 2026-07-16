from flask import Flask, request, redirect, session, render_template_string
import sqlite3
import bcrypt

app = Flask(__name__)
app.secret_key = "secure_login_system"

# -------------------------------
# Create Database
# -------------------------------
conn = sqlite3.connect("users.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password BLOB NOT NULL
)
""")

conn.commit()
conn.close()

# -------------------------------
# Home Page
# -------------------------------
@app.route("/")
def home():
    if "user" in session:
        return render_template_string("""
        <html>
        <head>
        <title>Dashboard</title>
        </head>
        <body style="font-family:Arial;text-align:center;margin-top:60px;">
            <h1>Welcome {{user}}</h1>
            <h3>Login Successful</h3>
            <a href="/logout">
                <button style="padding:10px 20px;">Logout</button>
            </a>
        </body>
        </html>
        """, user=session["user"])

    return render_template_string("""
    <html>
    <head>
    <title>Secure Login System</title>
    </head>

    <body style="font-family:Arial;text-align:center;margin-top:60px;">

    <h1>Secure Login System</h1>

    <a href="/register">
        <button style="padding:10px 20px;">Register</button>
    </a>

    <br><br>

    <a href="/login">
        <button style="padding:10px 20px;">Login</button>
    </a>

    </body>
    </html>
    """)

# -------------------------------
# Register
# -------------------------------
@app.route("/register", methods=["GET","POST"])
def register():

    if request.method=="POST":

        username=request.form["username"].strip()
        password=request.form["password"]

        if username=="" or password=="":
            return "All fields are required."

        if len(username)<3:
            return "Username must contain at least 3 characters."

        if len(password)<6:
            return "Password must contain at least 6 characters."

        hashed_password=bcrypt.hashpw(
            password.encode(),
            bcrypt.gensalt()
        )

        conn=sqlite3.connect("users.db")
        cursor=conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO users(username,password) VALUES(?,?)",
                (username,hashed_password)
            )
            conn.commit()

        except sqlite3.IntegrityError:
            conn.close()
            return "Username already exists."

        conn.close()

        return redirect("/login")

    return render_template_string("""

    <html>
    <head>
    <title>Register</title>
    </head>

    <body style="font-family:Arial;text-align:center;margin-top:50px;">

    <h2>User Registration</h2>

    <form method="POST">

    Username<br>
    <input type="text" name="username" required>

    <br><br>

    Password<br>
    <input type="password" name="password" required>

    <br><br>

    <button type="submit">Register</button>

    </form>

    <br>

    <a href="/">Home</a>

    </body>
    </html>

    """)

# -------------------------------
# Login
# -------------------------------
@app.route("/login", methods=["GET","POST"])
def login():

    if request.method=="POST":

        username=request.form["username"]
        password=request.form["password"]

        conn=sqlite3.connect("users.db")
        cursor=conn.cursor()

        cursor.execute(
            "SELECT password FROM users WHERE username=?",
            (username,)
        )

        row=cursor.fetchone()

        conn.close()

        if row:

            stored_password=row[0]

            if bcrypt.checkpw(password.encode(),stored_password):

                session["user"]=username

                return redirect("/")

        return "Invalid Username or Password"

    return render_template_string("""

    <html>
    <head>
    <title>Login</title>
    </head>

    <body style="font-family:Arial;text-align:center;margin-top:50px;">

    <h2>User Login</h2>

    <form method="POST">

    Username<br>
    <input type="text" name="username" required>

    <br><br>

    Password<br>
    <input type="password" name="password" required>

    <br><br>

    <button type="submit">Login</button>

    </form>

    <br>

    <a href="/">Home</a>

    </body>
    </html>

    """)

# -------------------------------
# Logout
# -------------------------------
@app.route("/logout")
def logout():

    session.pop("user",None)

    return redirect("/")

# -------------------------------
# Run Application
# -------------------------------
if __name__=="__main__":
    app.run(debug=True)