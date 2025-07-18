from flask import Flask, render_template, request, redirect, session, flash
from flask_mysqldb import MySQL
import os
from werkzeug.utils import secure_filename
import MySQLdb


app = Flask(__name__)
app.secret_key = 'your_secret_key'


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Gopinath@123'
app.config['MYSQL_DB'] = 'matrimony'

mysql = MySQL(app)



UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route('/')
def index():
    return render_template('index.html')  

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        existing_user = cur.fetchone()

        if existing_user:
            flash("Email already registered. Please log in or use another email.")
            cur.close()
            return redirect('/signup')

        cur.execute("INSERT INTO users (email, password) VALUES (%s, %s)", (email, password))
        mysql.connection.commit()
        cur.close()

        session['email'] = email
        return redirect('/register')

    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        print("Login attempt:", email, password)

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email=%s AND password=%s", (email, password))
        user = cur.fetchone()
        cur.close()

        print("DB result:", user)

        if user:
            session['user_id'] = user[0]
            session['email'] = user[1]
            print("Login successful! Redirecting to /dash")
            return redirect('/dash')
        else:
            print("Login failed: no match found.")
            flash('Invalid email or password')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'email' not in session:
        return redirect('/login')

    if request.method == 'POST':
        full_name = request.form.get('full_name')
        age = request.form['age']
        gender = request.form['gender']
        location = request.form['location']
        religion = request.form['religion']
        language = request.form['language']
        bio = request.form['bio']
        phone = request.form.get('phone')  

        profile_photo = request.files.get('profile_photo')
        filename = None

        if profile_photo and allowed_file(profile_photo.filename):
            filename = secure_filename(profile_photo.filename)
            profile_photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        try:
            cur = mysql.connection.cursor()
            cur.execute("""
                UPDATE users 
                SET full_name=%s, age=%s, gender=%s, location=%s, religion=%s,
                    language_preference=%s, bio=%s, profile_photo=%s, phone=%s 
                WHERE email=%s
            """, (full_name, age, gender, location, religion, language, bio, filename, phone, session['email']))
            mysql.connection.commit()
            cur.close()
            return redirect('/dash')
        except Exception as e:
            print("Error during profile update:", e)
            flash("Something went wrong. Please try again.")
            return redirect('/register')

    return render_template('register.html')
 

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user_id' not in session:
        return redirect('/login')

    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    if request.method == 'POST':
        full_name = request.form.get('full_name')
        age = request.form.get('age')
        gender = request.form.get('gender')
        location = request.form.get('location')
        religion = request.form.get('religion')
        language = request.form.get('language_preference')
        bio = request.form.get('bio')
        phone = request.form.get('phone')

        profile_photo = request.files.get('profile_photo')
        filename = None

        if profile_photo and allowed_file(profile_photo.filename):
            filename = secure_filename(profile_photo.filename)
            profile_photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        if filename:
            cur.execute("""
                UPDATE users 
                SET full_name=%s, age=%s, gender=%s, location=%s, religion=%s,
                    language_preference=%s, bio=%s, phone=%s, profile_photo=%s 
                WHERE id=%s
            """, (full_name, age, gender, location, religion, language, bio, phone, filename, session['user_id']))
        else:
            cur.execute("""
                UPDATE users 
                SET full_name=%s, age=%s, gender=%s, location=%s, religion=%s,
                    language_preference=%s, bio=%s, phone=%s 
                WHERE id=%s
            """, (full_name, age, gender, location, religion, language, bio, phone, session['user_id']))

        mysql.connection.commit()

    
    cur.execute("SELECT * FROM users WHERE id=%s", (session['user_id'],))
    user = cur.fetchone()
    cur.close()

    return render_template('profile.html', user=user)

@app.route('/dash')
def dash():
    if 'user_id' not in session:
        return redirect('/login')

    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)


    cur.execute("SELECT * FROM users WHERE id = %s", (session['user_id'],))
    user = cur.fetchone()

    if not user:
        flash("User not found. Please log in again.")
        return redirect('/login')

    
    search = request.args.get('search')
    age_from = request.args.get('age_from')
    age_to = request.args.get('age_to')
    location = request.args.get('location')

    
    query = "SELECT * FROM users WHERE id != %s AND gender != %s"
    values = [session['user_id'], user['gender']]

    if search:
        query += " AND (full_name LIKE %s OR location LIKE %s)"
        values.extend(['%' + search + '%', '%' + search + '%'])

    if age_from:
        query += " AND age >= %s"
        values.append(age_from)

    if age_to:
        query += " AND age <= %s"
        values.append(age_to)

    if location:
        query += " AND location LIKE %s"
        values.append('%' + location + '%')

    cur.execute(query, tuple(values))
    profiles = cur.fetchall()
    cur.close()

    return render_template('dash.html', profiles=profiles, user=user)
@app.route('/profile/<int:user_id>')
def view_profile(user_id):
    if 'user_id' not in session:
        return redirect('/login')

    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    profile = cur.fetchone()
    cur.close()

    if not profile:
        return "Profile not found", 404

    return render_template('view_profile.html', profile=profile)


@app.route('/delete_account', methods=['POST'])
def delete_account():
    if 'user_id' not in session:
        return redirect('/login')

    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM users WHERE id = %s", (session['user_id'],))
        mysql.connection.commit()
        cur.close()
        
        
        session.clear()
        flash("Your account has been deleted successfully.")
        return redirect('/')
    except Exception as e:
        print("Account deletion error:", e)
        flash("Something went wrong. Please try again.")
        return redirect('/profile')




@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
if __name__ == '__main__':
    app.run(debug=True)
