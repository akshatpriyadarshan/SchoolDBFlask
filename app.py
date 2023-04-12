from flask import Flask, render_template, session, redirect, url_for, flash
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
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        # Query the database to check if the user exists
        cur = mysql.connect().cursor()
        cur.execute('SELECT * from user_login where user_name=%s and user_password=%s', (username, password))
        user = cur.fetchone()
        cur.close()

        if user:
            # if the user exists set the session variable to their access level
            session['user_access_level'] = user['user_access_level']
            return redirect(url_for('index'))
        else:
            flash('Invalid Username & Password')
    return render_template('login.html', form=form)


@app.route('/home')
def home():  # put application's code here

    cursor = mysql.connect().cursor()
    cursor.execute('SELECT iduser_login,user_name, user_email,user_access_level from school.user_login ;')
    data = cursor.fetchone()
    print(data)
    if data is not None:
        print(data)
        return 'Data loaded is ' + str(data[0]) + data[1] + data[2] + str(data[3])
    else:
        return 'My database is not connected'


#    return render_template('index.html')


if __name__ == '__main__':
    app.run()
