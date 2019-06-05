from flask import Flask, render_template, request
from flask_mysqldb import MySQL
import json
app = Flask(__name__)

# We first specify the details of our sql server

app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'MyDB'

mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def index():

    #This gets user input from the html page and stores it in different variables

    if request.method == "POST":
        details = request.form
        userid = details['uid']
        tstamp = details['tsp']
        latlong = details['ll'] 
        noun = details['nn']
        verb = details['vb']
        time = details['tm']
        properties = details['pts']

    # This is to extract the value of the payment from the metadata

        json_acceptable_string = properties.replace("'", "\"")
        metadict = json.loads(json_acceptable_string)
        vlu = (metadict["value"])

    # We use this to create the database and insert values given by the user
        
        cur = mysql.connection.cursor()
        cur.execute("CREATE TABLE Eventt(usid INT(11), transactionid INT NOT NULL AUTO_INCREMENT,tsamp VARCHAR(20) NOT NULL,ltlong VARCHAR(15), non VARCHAR(10), vrb VARCHAR(10), timed VARCHAR(15), valu VARCHAR(1000), PRIMARY KEY(transactionid,usid));")
        cur.execute("INSERT INTO Eventt(usid,tsamp,ltlong,non,vrb,timed,valu) VALUES (%s,%s,%s,%s,%s,%s,%s);", (userid,tstamp,latlong,noun,verb,time,vlu))

        mysql.connection.commit()
        cur.close()
        assign()
        return 'success'
    return render_template('index.html')

def assign():

        #This generates an alert if a user makes a bill payment for the first time

        cur = mysql.connection.cursor()
        cur.execute("SELECT usid FROM Eventt WHERE (usid=(SELECT usid FROM Eventt ORDER BY transactionid DESC LIMIT 1)) GROUP BY usid, non, vrb HAVING (non='Bill' AND vrb='Pay' AND COUNT(*) = 1)")
        results = cur.fetchall()
        mysql.connection.commit()
        cur.close()
        for x in results:
            y = x[0]
            firstbillpayalert(y)

        #This generates an alert if the user makes 5 or more bill payments with total of at least 20000

        cur = mysql.connection.cursor()
        cur.execute("SELECT usid FROM Eventt GROUP BY usid, non, vrb HAVING (non='Bill' AND vrb='Pay' AND SUM(valu) >= 20000 AND COUNT(*) >= 5))")
        results = cur.fetchall()
        mysql.connection.commit()
        cur.close()
        for x in results:
            y = x[0]
            fiveormore(y)

        #This generates an alert if the user has made a payment but has not recieved feedback

        cur = mysql.connection.cursor()
        cur.execute("SELECT usid FROM Eventt Where (non='Bill' AND vrb='Pay' AND usid=(SELECT usid FROM Eventt Where (non='FDBK' AND vrb='Post')GROUP BY usid, ltlong HAVING (COUNT(*)=1)))GROUP BY usid, ltlong HAVING (COUNT(*)=1)")
        results = cur.fetchall()
        mysql.connection.commit()
        cur.close()
        if (len(results)==0):
            print("User ID's not in results have not gotten feedback")
            nofeedback()

def firstbillpayalert(userid):

    f = open("logs.txt","a")
    f.write("User" + str(userid)+ "made her first bill pay\n")

def fiveormore(userid):
    f = open("logs.txt","a")
    f.write("User" + str(userid) + "made 5 or more payments with total more than/equal to 20000 withing 5 minutes\n")

def nofeedback():
    f = open("logs.txt","a")
    f.write("Payment made but nofeedback given to user\n")

if __name__ == '__main__':
    app.run(debug=True)