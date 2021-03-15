from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_email import send_email 
from sqlalchemy.sql import func

app=Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:123456@localhost/height_collector'

app.config['SQLALCHEMY_DATABASE_URI']='postgres://nxaovhbhqfgagg:5d0b5f3bb57bde6d8a6d72d0dc0b78b531b6e91efff3cab73f0be4e0895fd948@ec2-3-211-37-117.compute-1.amazonaws.com:5432/de8jvb5afh1j6k?sslmode=require'
db=SQLAlchemy(app)

class Data(db.Model):
    __tablename__="data"
    id=db.Column(db.Integer, primary_key=True)
    email=db.Column(db.String(120), unique=True)
    height=db.Column(db.Integer)

    def __init__(self,email_,height_):
        self.email=email_
        self.height=height_


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/success",  methods=['POST'])
def success():
    if request.method=='POST':
        email=request.form['email_name']
        height=request.form['height_name']
        
        # print(email,height) 
        if db.session.query(Data).filter(Data.email==email).count()==0:
            data=Data(email,height)
            db.session.add(data)
            db.session.commit()
            average_height=db.session.query(func.avg(Data.height)).scalar()
            average_height=round(average_height,1)
            count=db.session.query(Data.height).count()
            send_email(email, height, average_height,count)
            return render_template("success.html")
        return render_template('index.html',text="seems like we've something from that email address already!")
if __name__=='__main__':
    app.debug=True
    app.run()

