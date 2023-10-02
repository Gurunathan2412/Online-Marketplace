from market import db, bcrypt,login
from flask_login import UserMixin


@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email = db.Column(db.String(length=50), nullable=False, unique=True)
    password = db.Column(db.String(length=60), nullable=False)
    budget = db.Column(db.Integer(), nullable=False, default=100000)
    items = db.relationship('Item',backref='owned_user', lazy=True)

    @property
    def pretty(self):
        if len(str(self.budget)) >= 4:
            return "{:,}".format(self.budget)

    @property
    def password_real(self):
        return self.password_real

    @password_real.setter
    def password_real(self,plain):
        self.password = bcrypt.generate_password_hash(plain).decode('utf-8')

    def check_password(self,attempted_password):
        return bcrypt.check_password_hash(self.password,attempted_password)

    def can_purchase(self,item):
        return self.budget >= item.price

    def can_sell(self,item):
        return item in self.items


class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    price = db.Column(db.Integer(), nullable=False)
    barcode = db.Column(db.String(length=12), nullable=False, unique=True)
    description = db.Column(db.String(length=1024), nullable=False, unique=True)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))

    def __repr__(self):
        return f'Item {self.name}'

    def buy(self,user):
        self.owner = user.id
        user.budget -= self.price
        db.session.commit()

    def sell(self,user):
        self.owner = None
        user.budget += self.price
        db.session.commit()
