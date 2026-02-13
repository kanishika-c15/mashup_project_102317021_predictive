from flask import Flask, render_template, request
import os
import zipfile
import validators
from flask_mail import Mail, Message

app = Flask(__name__)

# ---------- EMAIL CONFIG ----------
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'kkanishika_be23@thapar.edu'
app.config['MAIL_PASSWORD'] = 'ulor cacb pnyb gząh'

mail = Mail(app)

# ---------- ROUTES ----------
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        singer = request.form['singer']
        videos = request.form['videos']
        duration = request.form['duration']
        email = request.form['email']

        # Validation
        if not validators.email(email):
            return "Invalid Email ID"

        # Run Program 1
        cmd = f'python 102317022.py "{singer}" {videos} {duration} mashup.mp3'
        os.system(cmd)

        # Zip the output
        zip_name = "result.zip"
        with zipfile.ZipFile(zip_name, 'w') as zipf:
            zipf.write("mashup.mp3")

        # Send Email
        msg = Message(
            subject="Your Mashup File",
            sender=app.config['MAIL_USERNAME'],
            recipients=[email]
        )
        msg.body = "Your mashup is attached in ZIP format."
        with open(zip_name, 'rb') as f:
            msg.attach(zip_name, "application/zip", f.read())

        mail.send(msg)

        return "Mashup created and sent to your email successfully!"

    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)
import os
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
