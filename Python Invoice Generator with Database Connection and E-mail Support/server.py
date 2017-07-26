import os
import sys
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
import datetime
import time
import smtplib
import pymysql.cursors
from flask import Flask, render_template, request
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))


@app.route("/")
def main():
    return render_template("index.html")



# createpdf function to create a Invoice PDF
def cratepdf(companynamepdf, companyaddresspdf, amountpdf, staxpdf, emailpdf, timestamppdf, canvas2, datepdf, finalstaxpdf, productpdf):
    canvas = canvas2.Canvas("/home/raj/Documents/MyProjects/Python Invoice Generator with Database Connection and E-mail Support/INVOICE/Invoice (" + str(timestamppdf) + ").pdf", pagesize=letter)
    canvas.setLineWidth(.3)
    canvas.setFont('Helvetica', 12)
    canvas.line(50, 747, 580, 747) #FROM TOP 1ST LINE
    canvas.drawString(280, 750, "INVOICE")
    canvas.drawString(60, 720, "COMPANY NAME:- "+ companynamepdf)
    canvas.drawString(60, 690, "EMAIL-ID:- "+ emailpdf)
    canvas.drawString(60, 660, "ADDRESS:- "+ companyaddresspdf)
    canvas.drawString(450, 720, "DATE :- "+ str(datepdf))
    canvas.line(450, 710, 560, 710)
    canvas.line(50, 640, 580, 640)#FROM TOP 2ST LINE
    canvas.line(50, 748, 50, 50)#LEFT LINE
    canvas.line(400, 640, 400, 50)# MIDDLE LINE
    canvas.line(580, 748, 580, 50)# RIGHT LINE
    canvas.drawString(475, 615, 'TOTAL AMOUNT')
    canvas.drawString(100, 615, 'PRODUCT')
    canvas.line(50, 600, 580, 600)#FROM TOP 3rd LINE
    canvas.drawString(60, 550, productpdf)
    canvas.drawString(500, 550, amountpdf)
    TOTAL = int(amountpdf) * ((int(staxpdf)) / 100)
    canvas.drawString(60, 500, "SERVICE TAX (" +staxpdf+"%)")
    canvas.drawString(500, 500, str(TOTAL))
    canvas.line(50, 100, 580, 100)#FROM TOP 4th LINE
    canvas.drawString(60, 80, " TOTAL AMOUNT")
    canvas.drawString(500, 80, str(finalstaxpdf))
    canvas.line(50, 50, 580, 50)#FROM TOP LAST LINE
    canvas.save()


# addtodatabase function to add data to a mysql database
def addtodatabase(companynamedatabase, companyaddressdatabase, amountdatabase, emaildatabase, finalstaxdatabase, productdatabase):
    # Connect to the database
    connection = pymysql.connect(host='localhost',
                                 user='YOUR USER ID',
                                 password='PASSWORD',
                                 db='DATABASE NAME',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            # Create a new record
            sql = "INSERT INTO `YOUR TABLE NAME` (`Company_Name`,`Company_Address`,`Email_ID`, `Amount`, Final_Amount, Product) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (str(companynamedatabase), str(companyaddressdatabase), str(emaildatabase), str(amountdatabase), str(finalstaxdatabase), str(productdatabase)))
        connection.commit()
    finally:
        connection.close()





# sendemail function to send a E-mail
def sendemail(emailsendemail, Invoicename1, productsendemail):
    COMMASPACE = ', '
    def main():
        sender = 'Your E-Mail ID'
        gmail_password = 'Your E-Mail ID Password'
        recipients = [str(emailsendemail)]

        # Create the enclosing (outer) message
        outer = MIMEMultipart()
        outer['Subject'] = ' Invoice Details of product:-'+productsendemail
        outer['To'] = COMMASPACE.join(recipients)
        outer['From'] = sender
        outer.preamble = 'You will not see this in a MIME-aware mail reader.\n'

        # List of attachments
        attachments = [str(Invoicename1)]

        # Add the attachments to the message
        for file in attachments:
            try:
                with open(file, 'rb') as fp:
                    msg = MIMEBase('application', "octet-stream")
                    msg.set_payload(fp.read())
                encoders.encode_base64(msg)
                msg.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file))
                outer.attach(msg)
            except:
                print("Unable to open one of the attachments. Error: ", sys.exc_info()[0])
                raise

        composed = outer.as_string()

        # Send the email
        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as s:
                s.ehlo()
                s.starttls()
                s.ehlo()
                s.login(sender, gmail_password)
                s.sendmail(sender, recipients, composed)
                s.close()
            print("Email sent!")
        except:
            print("Unable to send the email. Error: ", sys.exc_info()[0])
            raise

    if __name__ == '__main__':
        main()


@app.route("/", methods=["POST"])
def Create():
    target = os.path.join(APP_ROOT)
    companyname = request.form['CompanyName']
    companyaddress = request.form['CompanyAddress']
    amount = request.form['Amount']
    stax = request.form['STax']
    email = request.form['E-mailId']
    product = request.form['Product']
    date = time.strftime("%d/%m/%Y")
    timestamp = datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p")
    Invoicename = "/home/raj/Documents/MyProjects/Python Invoice Generator with Database Connection and E-mail Support/INVOICE/Invoice ("+str(timestamp)+").pdf"
    finalstax = int(amount) + (int(amount) * ((int(stax))/100))
    cratepdf(companyname, companyaddress, amount, stax, email,timestamp, canvas, date, finalstax, product)
    addtodatabase(companyname, companyaddress, amount, email, finalstax, product)
    sendemail(email, Invoicename, product)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)