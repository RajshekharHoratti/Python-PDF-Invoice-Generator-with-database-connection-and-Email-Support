# Python-PDF-Invoice-Generator-with-database-connection-and-Email-Support
This Program is written in Python Version 3.5.2

This is a Program to Generate a PDF Invoice with all the needed functionality such as 

1:- Invoice Generated in PDF Format
2:- Database Connection
3:- Email Support

Here we are getting data from a UI for developing which i have used HTML & JAVASCRIPT with BOOTSTRAP there are fields such as 

1:- COMPANY NAME 
2:- COMPANY ADDRESS
3:- EMAIL ADDRESS
4:- PRODUCT NAME:-
5:- AMOUNT:-
6:- SERVICE TAX:-

and after filling all the fields and submitting it.
It will directly store all the data in the database and craete a PDF Invoice file and stores it in the avaliable INVOICE folder and also sends a Email to the customer with the PDF Invoice file attached to it.

To start with you need to set up the Database with columns such as

1:- Coompnay_Name
2:- Company_Address
3:- Email_Id
4:- Amount
5:- Final_Amount
6:- Product

After setting up the database run the server.py file 

Python server.py

and then yo need to open the browser and type a URL
http://localhost:8080/

OR

http://0.0.0.0:8080/

