from flask import Flask, render_template
from flaskext.mysql import MySQL


# my db connection
local_sever = True
app = Flask(__name__)

app.secret_key = 'ramprasadchaudharyschool'
# db connection
mysql = MySQL()
app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Akshat@11'
app.config['MYSQL_DATABASE_DB'] = 'school'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


# Creating DB models
# class Login(db.Model):
#     id = db.Column(db.INTEGER, primary_key=True)
#     name = db.Column(db.String(100))
#     email = db.Column(db.String(100))


@app.route('/')
def main():  # put application's code here
    return render_template('index.html')


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
