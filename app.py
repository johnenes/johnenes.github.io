from flask import Flask, render_template, request, flash, redirect, url_for
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from model import OldDayChickModel
from services import Auth
from extensions import db

app = Flask(__name__)
app.config['SECRET_KEY'] = "YouDontGetTheKey"
app.config['SQLALCHEMY_DATABASE_URL'] = 'sqlite:////app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


@app.route('/')
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        pswd = request.form.get('password')

        msg, status = Auth.login(email, pswd)

        if status == 200:
            flash(message=msg)
            return redirect(url_for('login.html'))
        
    return render_template('')


def index():
    return render_template('index.html')


@app.route('/register')
def customer_register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        pnumber = request.form.get('pnumber')
        password = request.form.get('password')

        message, status = Auth.user_register(
            name=name, email=email, password=password,
            pnumber=pnumber
            )
        
        if status == 200:
            flash(message=f'{message} successfully registered.')
            return render_template('booking.html')
        
        elif status == 400:
            flash(message=f"{message} user doesn't exist")

        
        
    return render_template('registration.html')
    

 
@staticmethod
def old_day_chicks(order_date: datetime, 
    preffered_date: datetime,
    chick_type: str, 
    breed_type: str
 ):
        """Validate input types"""
        if not isinstance(order_date, datetime) or not isinstance(preffered_date, datetime):
            return {"error": "Invalid date format"}, 400
        
        if not isinstance(chick_type, str) or not isinstance(breed_type, str):
            return {"error": "Invalid type for chick_type or breed_type"}, 400
        
        """Create a new OldDayChickModel instance"""
        customer_booking = OldDayChickModel(
            order_date=order_date,
            preffered_date=preffered_date,
            chick_type=chick_type,
            breed_type=breed_type
        )
        
        try:
            """Add the instance to the session and commit"""
            db.session.add(customer_booking)
            db.session.commit()
            """Return a success response with relevant data"""
            return {
                "order_date": customer_booking.order_date.isoformat(),
                "preffered_date": customer_booking.preffered_date.isoformat(),
                "chick_type": customer_booking.chick_type,
                "breed_type": customer_booking.breed_type
            }, 201
        except IntegrityError as e:
            """Rollback the session in case of error"""
            db.session.rollback()
            """Return the error message and a status code"""
            return {"error": str(e)}, 422



app.run()

