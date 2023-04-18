from flask import Flask, render_template, session, redirect, url_for, flash, request
from flaskext.mysql import MySQL
import yaml

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

# my db connection
local_sever = True
app = Flask(__name__)

app.secret_key = 'ramprasadchaudharyschool'

# load the database configuration from YAML file
db_config = yaml.load(open('config.yaml'), Loader=yaml.FullLoader)

app.config['MYSQL_HOST'] = db_config['mysql']['host']
app.config['MYSQL_USER'] = db_config['mysql']['user']
app.config['MYSQL_PASSWORD'] = db_config['mysql']['password']
app.config['MYSQL_DB'] = db_config['mysql']['database']
app.config['MYSQL_DATABASE_USER'] = 'aksha'
app.config['MYSQL_DATABASE_PASSWORD'] = '11031986'
app.config['MYSQL_DATABASE_DB'] = 'School'

mysql = MySQL(app)
mysql.init_app(app)


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')


@app.route('/')
def index():  # put application's code here
    access_level = session.get('user_access_level')
    if access_level is None:
        return redirect(url_for('login'))
    else:
        return redirect(url_for('home'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    # print(app.config)
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        # Query the database to check if the user exists
        cur = mysql.connect().cursor()
        if cur is not None:
            cur.execute('SELECT * from user_login where user_name=%s and user_password=%s', (username, password))
            user = cur.fetchone()
            # print(user)
            cur.close()
        else:
            return 'My database is not connected'

        if user:
            # if the user exists set the session variable to their access level
            session['user_access_level'] = user[4]
            return redirect(url_for('index'))
        else:
            flash('Invalid Username & Password')
    return render_template('login.html', form=form)


@app.route('/home')
def home():  # put application's code here

    return render_template('home.html')


@app.route('/student')
def student():  # put application's code here

    return render_template('student.html')


@app.route('/search-student', methods=['GET', 'POST'])
def search_student():
    if request.method == 'POST':
        # Get the student ID from the search form
        student_id = request.form['student_id']

        if student_id:
            # Search for the student in the database
            cur = mysql.connect().cursor()
            query = "SELECT * FROM student WHERE idStudent = %s"
            cur.execute(query, (student_id,))
            student_details = cur.fetchone()

            # If the query returned a row, display the student data
            if student_details:
                # print(student_details)
                return render_template('student.html', student=student_details)
            else:
                # If the query did not return any rows, display a flash message
                flash('No data found for Student ID {}'.format(student_id))

    return render_template('student.html')


@app.route('/add-student', methods=['GET', 'POST'])
def add_student():
    # Handle the form submission to add a new student to the database
    print("in add_student")
    if request.method == 'POST':
        # Get the form data from the request
        print("request is POST")
        student_id = int(request.form['student_id'])
        student_admno = int(request.form['student_admno'])
        student_tcno = request.form['student_tcno']
        student_withdrawalno = request.form['student_withdrawalno']
        student_firstname = request.form['student_firstname']
        student_middlename = request.form['student_middlename']
        student_lastname = request.form['student_lastname']
        student_dob = request.form['student_dob']
        student_gender = request.form['student_gender']
        student_fathername = request.form['student_fathername']
        student_mothersname = request.form['student_mothersname']
        student_contactnum = request.form['student_contactnum']
        student_address = request.form['student_address']
        student_joiningclass = request.form['student_joiningclass']
        student_currclass = request.form['student_currclass']
        student_joiningdate = request.form['student_joiningdate']
        student_exitdate = request.form['student_exitdate']
        student_fatheroccupation = request.form['student_fatheroccupation']
        student_currsession = request.form['student_currsession']
        student_image = request.form['student_image']

        # Validate the form data
        if not student_admno or not student_tcno:
            flash('Please fill in all required fields.')
            return redirect(url_for('add_student'))

        # Insert the data into the database
        cur = mysql.connect().cursor()
        print(cur)
        insert_query = "INSERT INTO student (idStudent, Student_admno, Student_tcno, Student_withdrawalno, " \
                       "Student_firstname, Student_middlename, Student_lastname, Student_dob, student_gender, " \
                       "Student_fathername, Student_mothersname, Student_contactnum, Student_address, " \
                       "Student_joiningclass, Student_currclass, Student_joiningdate, Student_exitdate, " \
                       "Student_fatheroccupation, Student_currsession, student_image) " \
                       "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        try:
            cur.execute(insert_query, (student_id, student_admno, student_tcno, student_withdrawalno, student_firstname,
                                       student_middlename, student_lastname, student_dob, student_gender,
                                       student_fathername, student_mothersname, student_contactnum, student_address,
                                       student_joiningclass, student_currclass, student_joiningdate, student_exitdate,
                                       student_fatheroccupation, student_currsession, student_image))
            mysql.connect().commit()

            print(student_id, student_admno, student_tcno, student_withdrawalno, student_firstname, student_middlename,
                  student_lastname, student_dob, student_gender, student_fathername, student_mothersname,
                  student_contactnum, student_address, student_joiningclass, student_currclass, student_joiningdate,
                  student_exitdate, student_fatheroccupation, student_currsession, student_image)
        except mysql.connect().Error as err:
            print(err)
            print("Error Code:", err.errno)
            print("SQLSTATE", err.sqlstate)
            print("Message", err.msg)
        except mysql.connect().ProgrammingError as err:
            print(err)
        except (mysql.connect().IntegrityError, mysql.connect().DataError) as err:
            print("DataError or IntegrityError")
            print(err)
        finally:
            mysql.connect().close()
            print('New student added successfully.')

        # Redirect the user back to the student page
        return redirect(url_for('student'))
    else:
        # If the request is a GET request, just render the add student form
        return render_template('add_student.html')


@app.route('/teachers')
def teachers():  # put application's code here

    return render_template('teachers.html')


@app.route('/fees')
def fees():  # put application's code here

    return render_template('fees.html')


@app.route('/notices')
def notices():  # put application's code here

    return render_template('notice.html')


if __name__ == '__main__':
    app.run()
