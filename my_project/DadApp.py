from flask import Flask, render_template, request
import smtplib
from email.mime.text import MIMEText
import os

app = Flask(__name__)

# تنظیمات ایمیل از متغیرهای محیطی
SENDER_EMAIL = "meisamabd02@gmail.com"
EMAIL_PASSWORD = "mfko mwwp chnf rage"

# لیست موقت برای ذخیره اطلاعات کاربران
users = []


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        father_name = request.form['father_name']
        melli_code = request.form['melli_code']
        phone_number = request.form['phone_number']
        land_line = request.form['land_line']
        province = request.form['province']
        city = request.form['city']
        district = request.form['district']
        street = request.form['street']
        alley = request.form['alley']
        plaque = request.form['plaque']

        # ذخیره در لیست موقت
        users.append({
            "first_name": first_name,
            "last_name": last_name,
            "father_name": father_name,
            "melli_code": melli_code,
            "phone_number": phone_number,
            "land_line": land_line,
            "province": province,
            "city": city,
            "district": district,
            "street": street,
            "alley": alley,
            "plaque": plaque
        })

        # ارسال ایمیل
        send_email(first_name, last_name, father_name, melli_code, phone_number, land_line, province, city, district,
                   street, alley, plaque)

        return "اطلاعات شما ثبت شد و ارسال گردید!"

    return render_template("index2.html", users=users)


def send_email(first_name, last_name, father_name, melli_code, phone_number, land_line, province, city, district,
               street, alley, plaque):
    if not SENDER_EMAIL or not EMAIL_PASSWORD:
        print("ایمیل و پسورد تنظیم نشده است!")
        return

    receiver_email = SENDER_EMAIL

    message = MIMEText(
        f"name: {first_name}\nfamily: {last_name}\nfather_name: {father_name}\n"
        f"melli_code: {melli_code}\nphone: {phone_number}\nland_line: {land_line}\n"
        f"province: {province}\ncity: {city}\ndistrict: {district}\n"
        f"street: {street}\nalley: {alley}\nplaque: {plaque}"
    )
    message['Subject'] = 'اطلاعات جدید کاربر'
    message['From'] = SENDER_EMAIL
    message['To'] = receiver_email

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, EMAIL_PASSWORD)
        server.sendmail(SENDER_EMAIL, receiver_email, message.as_string())
        server.quit()
    except Exception as e:
        print("خطا در ارسال ایمیل:", e)


if __name__ == '__main__':
    app.run(debug=True)
