import pandas as pd
from selenium import webdriver
import numpy as np
import os
from flask import Flask, session, render_template
from flask_mail import Mail


app = Flask(__name__)

# configuration of mail
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'codescatter8980@gmail.com'
app.config['MAIL_PASSWORD'] = 'ynqolwjdibmzudao'
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)



def get_screened_stocks(url, name):

    driver = webdriver.Chrome(executable_path='C:/Users/admin/Desktop/general_screener/chromedriver')
    driver.get(url)
    
    l = driver.find_element("xpath",'//*[@id="root"]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div[1]/button[1]')
    l.click()
    table = pd.read_html(driver.find_element("xpath",'//*[@id="DataTables_Table_0"]').get_attribute('outerHTML'))
    driver.close()

    if name=="below":
        mail.send_message("Stock Market",
                            sender="hgadhiya8980@gmail.com",
                            recipients=["harshitgadhiya8980@gmail.com"],
                            body='table is below condition {}'.format(table[0]))
    else:
        mail.send_message("Stock Market",
                          sender="hgadhiya8980@gmail.com",
                          recipients=["harshitgadhiya8980@gmail.com"],
                          body='table is above condition {}'.format(table[0]))

    return table[0]

@app.route("/", methods=["GET","POST"])
def home():
    url = "https://chartink.com/screener/mypersonal-3"
    get_screened_stocks(url, "above")

    url = "https://chartink.com/screener/mypersonal-below"
    get_screened_stocks(url, "below")
    return render_template("index.html") 

if __name__ == "__main__":
    # db.create_all()
    app.run(
        host='127.0.0.1',
        port='5000',
        debug=True)

