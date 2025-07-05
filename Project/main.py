from datetime import datetime
from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from email.message import EmailMessage
import send_Email


app = Flask(__name__)

#specify parameters (config dictionary) of the database
app.config["SECRET_KEY"] = "myapplication123"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
db = SQLAlchemy(app)

#Create a database
#first create database model using class
#inherits from db.Model
#executing the class to an object creates the table from the table model described
class Form(db.Model):
    #db.Column() is used to add columns to the table and the type of data
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    email = db.Column(db.String(80))
    date = db.Column(db.Date)
    occupation = db.Column(db.String(80))


class Emaildata():
    def __init__(self, recipient_fname, recipient_lname, email_addr, date):
        self.recipient_fname = recipient_fname
        self.recipient_lname = recipient_lname  
        self.email_addr = email_addr
        self.date = date

        print(f"runtime log2: called Emaildata constructor and initialized the Emaildata class\n")
        print(f"variables create: {self.recipient_fname} {self.date}")

       
    def make_email(self):
        self.email_message = EmailMessage()
        email_string = f"""Good Day {self.recipient_fname} {self.recipient_lname},

        You have successfully submitted the job application form for the position of CEO of The UN on {self.date}.
        Good luck!

        Best Regards,
        The UN HR
        """

        self.email_message["Subject"] = "Application form submitted"
        self.email_message["From"] = "org.imj.yyc@gmail.com"
        self.email_message["To"] = "imjogiat@gmail.com"

        self.email_message.set_content(email_string)

        print(f"runtime log3: emailmessage object created and data set")
    
    def send_email(self):
        send_Email.email(self.email_message)
        print(f"runtime log4: called send_email method then called email method within send_Email library")
    

#decorator that calls the function defined below
#when a user goes to the default main html page, call the function below
#GET and POST are defined as methods/requests that will prompt an output
@app.route("/", methods=["GET","POST"])
def index():
    print(request.method)
    if request.method == "POST":
        #the flask request object has a variable "form", this form requires
        #the name of the tag (input tag name parameter) and returns the value
        #entered into that input  -this only works for input tags
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email_address = request.form["email"]
        start_date_str = request.form["date"]
        date_obj = datetime.strptime(start_date_str, "%Y-%m-%d")
        occupation = request.form["occupation"]

        #class constructor arguments/paramaters don't need to be defined
        #in the class, since they are defined in the parent constructor
        form = Form(first_name=first_name, last_name=last_name,
                    email=email_address, date=date_obj,
                    occupation=occupation)
        #adds the form object (fills in the table mold) to the database
        #this fills in the columns of the table for a particular row
        print("runtime log1: calling Emaildata method")

        Email_form = Emaildata(recipient_fname=first_name, recipient_lname=last_name, 
                  email_addr=email_address, date=start_date_str)
        Email_form.make_email()
        Email_form.send_email()

        print(f"runtime log5: email sent and program returned to index method")
        
        db.session.add(form)
        db.session.commit()
        flash("Your form was submitted successfully!", "success")

    return render_template("index.html")

if __name__ == "__main__":
    with app.app_context():
        #this checks for an existing database and if one doesn't exist,
        #it creates one
        db.create_all()
        app.run(debug=True, port=5001)