from market import app,render_template,db
from market.models import Item,User
from flask import redirect,url_for,flash, request
from market.forms import RegisterForm,Login,Purchase, Sell
from flask_login import login_user, logout_user, login_required, current_user


@app.route('/')
@app.route('/home')
def home_page():
    return render_template("home.html")


@app.route('/market', methods=['GET','POST'])
@login_required
def market_page():
    purchase = Purchase()
    sell = Sell()
    if request.method == "POST":
        #Purchase
        purchased_item = request.form.get("purchased_item")
        p_item_obj = Item.query.filter_by(name=purchased_item).first()
        if p_item_obj:
            if current_user.can_purchase(p_item_obj):
                p_item_obj.buy(current_user)
                flash(f"Congratulations! You purchased {p_item_obj.name} for ₹{p_item_obj.price}" ,category="success")
            else:
                flash(f"Unfortunately, you don't have enough money to purchase {p_item_obj.name}", category="danger")

        #Sell
        sold_item = request.form.get("sold_item")
        s_item_obj = Item.query.filter_by(name=sold_item).first()
        if s_item_obj:
            if current_user.can_sell(s_item_obj):
                s_item_obj.sell(current_user)
                flash(f"You successfully sold the item {s_item_obj.name}", category="success")
            else:
                flash(f"Something went wrong with selling {p_item_obj.name}", category="danger")

        return redirect(url_for("market_page"))
    if request.method == "GET":
        items = Item.query.filter_by(owner=None)
        owned_items = Item.query.filter_by(owner=current_user.id)

        return render_template("market.html", items=items, purchase=purchase, owned_items=owned_items, sell=sell)


@app.route('/register', methods=['GET','POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    email=form.email.data,
                    password_real=form.password1.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash(f"Account created successfully! You are now logged in as: {user.username}", category="success")
        return redirect(url_for("market_page"))
    if form.errors != {}:
        for err in form.errors.values():
            flash(f"There is an error: {err}", category='danger')

    return render_template("register.html", form=form)


@app.route('/login', methods=['GET','POST'])
def login_page():
    form = Login()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(attempted_password=form.password.data):
            login_user(user)
            flash(f"Successfully Logged in: {user.username}", category="success")
            return redirect(url_for("market_page"))
        else:
            flash(f"Username and Password not matched, try again!!", category="danger")

    return render_template("login.html",form=form)


@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out", category='info')
    return redirect(url_for("home_page"))
