from flask import Flask, render_template, redirect, url_for, session, request
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.sqla.fields import QuerySelectField
from flask_sqlalchemy import SQLAlchemy
from flask_admin.form.upload import FileUploadField

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
app.secret_key = 'your_secret_key'

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    fb = db.Column(db.String(120), unique=True)
    insta = db.Column(db.String(120), unique=True)
    twitter = db.Column(db.String(120), unique=True)
    photo = db.Column(db.String(255))
    sold = db.Column(db.String(255))
    earned = db.Column(db.String(255))
    diagnosis = db.Column(db.String(255))
    photos = db.relationship('Photos', backref='user', lazy=True)

class Photos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    photo = db.Column(db.String(255))

class UsersView(ModelView):
    column_list = ('id', 'username', 'fb', 'insta', 'photo', 'twitter','sold','earned','diagnosis')
    column_labels = {'sold':'Продано','earned':'Заработано','diagnosis':'Диагноз'}
    form_extra_fields = {
        'photo': FileUploadField('Photo', base_path='static/images', relative_path='images/')
    }
    create_template = 'create_user.html'
    def is_accessible(self):
        return session.get('logged_in')

class PhotosView(ModelView):
    column_list = ('id', 'photo', 'user')
    column_formatters = {'user': lambda view, context, model, name: model.user.username}
    form_extra_fields = {
        'photo': FileUploadField('Photo', base_path='static/images', relative_path='images/'),
        'user': QuerySelectField('User', query_factory=lambda: Users.query.all(), get_label='username')
    }
    create_template = 'create_photo.html'
    def is_accessible(self):
        return session.get('logged_in')

class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return session.get('logged_in')

admin = Admin(app, name='Admin Panel', template_mode='bootstrap3', index_view=MyAdminIndexView())
admin.add_view(UsersView(Users, db.session))
admin.add_view(PhotosView(Photos, db.session))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == 'admin':
            session['logged_in'] = True
            return redirect(url_for('admin.index'))
        else:
            return 'Invalid username or password'
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))

# @app.route('/user/<int:id>/')
# def show_user_info(id):
#     user = Users.query.get(id)
#     return render_template('name.html', user=user)

@app.route('/user/<int:id>/')
def show_user_info(id):
    user = Users.query.get(id)
    photos = Photos.query.filter_by(user_id=id).all()
    return render_template('name.html', user=user, photos=photos)

@app.route('/')
def index():
    return 'Welcome to the home page!'

if __name__ == '__main__':
    app.run(debug=True)
