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
