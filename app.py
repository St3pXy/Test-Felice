# Importing Libraries
from crypt import methods
from flask import Flask, g, redirect, render_template, request, url_for, session, flash, abort
import requests
import os
import sqlite3
import imghdr
import smtplib, ssl
import smtplib
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText


# Starting up Flask App
app = Flask(__name__, template_folder='./templates',
            static_folder='./templates/static')
# Creators: Backend: Step @step_xy | Frontend: Imam
app.secret_key = 'PremiumId-Official-Website'


#   Internal Functions

# Database Declaration
# User Provenience Database (Web | Instagram | Step)
conn = sqlite3.connect('user_data.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS user_data
             (web_users int, instagram_users int, step_users int)''')
conn.commit()

# User Tracking Database (ip adress)
conn = sqlite3.connect('user_ip_track.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS user_ip_track
             (user_data_info text)''')
conn.commit()

# User Tracking Database (user impressions)
conn = sqlite3.connect('user_impressions_track.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS user_impressions_track
             (user_link text, user_ip_adress text)''')
conn.commit()

# SendEmail

# TryalFunction
def sendEmail(subj, email, txt):

    print("Parametri: ", subj, "\n", email, "\n", txt)

    gmail_user = "Premiumidhead@gmail.com"
    gmail_password = ""

    sent_from = gmail_user
    to = ['Premiumidhead@gmail.com']
    subject = subj
    emailText = "OGGETTO: " + str(subject) + "\nEMAIL: " + email + "\n\nMESSAGGIO:\n" + txt + "\n"
    emailText = "\n" + emailText + "\n"
    body = emailText.encode('ascii', 'ignore').decode('ascii')

    print("EMAIL TEXT: ", emailText, "\n\nBODY: ", body)

    #email_text = """\
    #From: %s
    #To: %s
    #Subject: %s

    #%s
    #""" % (sent_from, ", ".join(to), subject, body)

    email_text = body

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, to, email_text)
        server.close()

        print('\nEmail sent!\n')
        return "ok"
    except Exception as e:
        print('Something went wrong...')
        return str(e)


def sendEmail_normal(subject, email, txt):

    email_adress = "Premiumidhead@gmail.com"  # PremiumID gmail email to read users messages
    email_password = ""  # PremiumID gmail email password

    #Legend:
    #   simple # comments as #<code> is from V1
    #   spaced # comments as # <code> is from V2
    #   complex # comments as #    <code> is from V3

    #msg = EmailMessage()
    #msg['Subject'] = subject
    #msg['From'] = email_adress
    #msg['To'] = email_adress

    email_text = "La comunicazione riguarda: " + subject + "\nL'email del mittente è: " + email + "\n\nIl suo messaggio è il seguente:\n" + txt + "\n"
    #msg.set_content(email_text)

    # port = 587  # For starttls
    # smtp_server = "smtp.gmail.com"
    # sender_email = "Premiumidhead@gmail.com"
    # receiver_email = "Premiumidhead@gmail.com"
    # password = ""
    # message = email_text

    # context = ssl.create_default_context()
    '''
    port = 587  # For starttls
    smtp_server = "smtp.gmail.com"
    sender_email = "Premiumidhead@gmail.com"
    receiver_email = "Premiumidhead@gmail.com"
    password = ""
    message = email_text

    try:

        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_server, port) as server:
            server.ehlo()  # Can be omitted
            server.starttls(context=context)
            server.ehlo()  # Can be omitted
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)

            return "ok"
    except Exception as e:
        print(e)
        return e
    '''

    msg = MIMEText(email_text)
    msg['Subject'] = subject
    msg['From'] = email_adress
    msg['To'] = email_adress

    # Send the message via our own SMTP server, but don't include the
    # envelope header.
    s = smtplib.SMTP()
    s.connect('smtp.gmail.com', 465)
    s.login(email_adress, email_password)
    s.connect()
    s.sendmail(email_adress, [email_adress], msg.as_string())
    s.quit()

    try:
        #with smtplib.SMTP_SSL('smtp.gmail.com', 587) as smtp:
        #with smtplib.SMTP('smtp.gmail.com', 465) as smtp:
        #    smtp.login(email_adress, email_password)
        #    smtp.send_message(msg)

        # with smtplib.SMTP(smtp_server, port) as server:
            # server.ehlo()  # Can be omitted
            # server.starttls(context=context)
            # server.ehlo()  # Can be omitted
            # server.login(sender_email, password)
            # server.sendmail(sender_email, receiver_email, message)

        return "ok"

    except Exception as e:
        phrase = "\n\n\nThe Following Error Occured: \n" + str(e)
        return phrase


def track_user_impressions():
    user_url = request.url
    user_ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)

    conn = sqlite3.connect('user_impressions_track.db')
    c = conn.cursor()
    c.execute('INSERT INTO user_impressions_track VALUES (?, ?)',
              [user_url, user_ip])
    conn.commit()

    # Debug
    print(user_url)
    print(user_ip)

    conn = sqlite3.connect('user_impressions_track.db')
    c = conn.cursor()
    c.execute(f'SELECT * FROM user_impressions_track')
    db_res = c.fetchall()
    print(db_res)


#   Website

# Get User Provvenience

@app.before_first_request
def do_something_only_once():

    # Get User Url
    user_url = request.url
    print(user_url)

    # Get User Ip
    user_ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)

    # Add User Ip to Database
    conn = sqlite3.connect('user_ip_track.db')
    c = conn.cursor()
    c.execute('INSERT INTO user_ip_track VALUES (?)', [user_ip])
    conn.commit()

    # Debug
    conn = sqlite3.connect('user_ip_track.db')
    c = conn.cursor()
    c.execute(f'SELECT * FROM user_ip_track')
    db_res = c.fetchall()
    print(db_res)

    # Get Data From DB
    conn = sqlite3.connect('user_data.db')
    c = conn.cursor()
    c.execute(f'SELECT * FROM user_data')
    db_res = c.fetchall()
    print(db_res)

    try:
        insta_user_value = db_res[0][1]
        insta_user_value += 1

    except IndexError:
        conn = sqlite3.connect('user_data.db')
        c = conn.cursor()
        c.execute('INSERT INTO user_data VALUES (?, ?, ?)', [0, 0, 0])
        conn.commit()

    conn = sqlite3.connect('user_data.db')
    c = conn.cursor()
    c.execute('UPDATE user_data SET instagram_users = (?) ', [insta_user_value])
    conn.commit()

    # Debug
    conn = sqlite3.connect('user_data.db')
    c = conn.cursor()
    c.execute(f'SELECT * FROM user_data')
    db_res = c.fetchall()
    print(db_res)

    return redirect(url_for("home"))


# Home

# Temporary Home
@app.route("/", methods=['GET', 'POST'])
def pre_release():
    if request.method == "POST":

        if "RichiediConsulenza" in request.form:
            nome = request.form["name"]
            pas = request.form["surname"]

            if nome == "PremiumIDPreReleasePage" and pas == "123St3p_!PremiumIdPassword":
                return redirect(url_for("home"))

            else:
                return redirect(url_for("pre_release"))

    else:
        #track_user_impressions()
        return render_template("pages/pre_release_page_password.html")


@app.route("/home", methods=['GET', 'POST'])
def home():
    if request.method == "POST":

        return redirect(url_for("home"))

    else:
        track_user_impressions()
        return render_template("pages/home.html")

'''
@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == "POST":

        return redirect(url_for("home"))

    else:
        track_user_impressions()
        return render_template("pages/home.html")
'''

@app.route("/chi_siamo", methods=['GET', 'POST'])
def chi_siamo():
    if request.method == "POST":
        pass

    else:
        return render_template("pages/chi_siamo.html")


@app.route("/servizi", methods=['GET', 'POST'])
def servizi():
    if request.method == "POST":
        pass

    else:
        return render_template("pages/servizi.html")


@app.route("/portfolio", methods=['GET', 'POST'])
def portfolio():
    if request.method == "POST":
        pass

    else:
        return render_template("pages/portfolio.html")


@app.route("/management", methods=['GET', 'POST'])
def management():
    if request.method == "POST":
        pass

    else:
        return render_template("pages/management.html")


@app.route("/portfolio/<project>", methods=['GET'])
def show_portfolio(project):
    try:
        if project in ['snipes', 'polo-club', 'genesi', 'farfetch']:
            return render_template(f"pages/portfolio/{project}.html")
    except:
        abort(404)
        return redirect(url_for("home"))

@app.route("/prenota_consulenza", methods=['GET', 'POST'])
def prenota_consulenza():
    if request.method == "POST":
        if "RichiediConsulenza" in request.form:
            nome = request.form["name"]
            surname = request.form["surname"]
            insta_nick = request.form["insta_name"]
            email = request.form["email"]
            company = request.form["company"]
            message = request.form["mess"]
            date = request.form["date"]
            print("Valori: \n", nome, "\n", surname, "\n", insta_nick,
                  "\n", email, "\n", company, "\n", message, "\n", date)

            user_input_data = "Inviato da " + nome + " " + surname + "\nUrl instagram: " + insta_nick + "\nEmail: " + email + "\nAzienda: " + company + "\nConsulenza per il: " + date + "\nHa inviato il seguente messaggio:\n\n" + message
            
            err = sendEmail("Prenotazione Consulenza", email, user_input_data)
            try:
                if err == "ok":
                    flash("Your message has been send successfully")
                else:
                    print(err)
                    flash("An error occured. Please try again.")
            except:
                flash("An error occured. Please try again.")

            return redirect(url_for("home"))

    else:
        return render_template("pages/consulenza.html")


@app.route("/lavora_con_noi", methods=['GET', 'POST'])
def lavora_con_noi():
    if request.method == "POST":

        if "Contattaci" in request.form:
            email = request.form["message_email"]
            message = request.form["message_message"]

            print(email)
            print(message)

            err = sendEmail("Messaggio Utente", email, message)

        elif "LavoraConNoi" in request.form:
            email = request.form["workWithUs_email"]
            message = request.form["workWithUs_message"]

            print(email)
            print(message)

            err = sendEmail("Lavora Con Noi Utente", email, message)

        try:
            print("ERR: " + str(err))
            if err == "ok":
                flash("Your message has been send successfully")
            else:
                print(err)
                flash("An error occured. Please try again.")
        except UnboundLocalError:
            flash("An error occured. Please try again.")

        return redirect(url_for("lavora_con_noi"))

    else:
        return render_template("pages/lavora_con_noi.html")


@app.route("/instagram", methods=['GET', 'POST'])
def instagram():
    if request.method == "POST":
        pass

    else:
        track_user_impressions()
        return redirect(url_for("home"))


@app.route("/step", methods=['GET', 'POST'])
def step():
    if request.method == "POST":
        pass

    else:
        track_user_impressions()
        return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)  # Testing Command
    # app.run()  # Official Run Command
