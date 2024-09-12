from model import UserModel, OldDayChickModel
from extensions import db
from sqlalchemy.exc import IntegrityError
from datetime import datetime

class Auth:
    def user_register(name, email, password, pnumber):
        user = UserModel(name=name, email=email, pnumber=pnumber)
        user.set_password(password=password)

        try:
            db.session.add(user)
            db.session.commit()

            return user.email, 200
        
        except IntegrityError as e:
            return e, 400
        
    def login(email, pswd):
        user = UserModel.query.filter_by(email=email).first()
        if (user is not None) and user.check_password(pswd):
            return 'Success', 200
        
        return 'Error', 401


 
class Booking:
        @staticmethod
        def old_day_chicks(order_date: datetime, preffered_date: datetime, chick_type: str, breed_type: str):
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
                """ Return a success response with relevant data"""
                return {
                    "order_date": customer_booking.order_date.isoformat(),
                    "preffered_date": customer_booking.preffered_date.isoformat(),
                    "chick_type": customer_booking.chick_type,
                    "breed_type": customer_booking.breed_type
                }, 201  
            except IntegrityError as e:
                """ollback the session in case of error"""
                db.session.rollback()
                """Return the error message and a status code"""
                return {"error": str(e)}, 422       
