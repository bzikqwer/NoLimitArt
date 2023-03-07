class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    fb = db.Column(db.String(120), unique=True)
    insta = db.Column(db.String(120), unique=True)