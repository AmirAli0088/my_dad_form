from flask import Flask, render_template, request
import smtplib
from email.mime.text import MIMEText
import socket

app = Flask(__name__)

SENDER_EMAIL = "meisamabd02@gmail.com"
EMAIL_PASSWORD = "mfko mwwp chnf rage"

users = []


def check_internet():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=5)
        return True
    except OSError:
        return False


def is_valid_number(value, length):
    return value.isdigit() and len(value) == length


def is_valid_text(value, min_length=3):
    return len(value) >= min_length


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        required_fields = ['first_name', 'last_name', 'father_name', 'melli_code', 'phone_number_1', 'land_line',
                           'province', 'city', 'district', 'street', 'alley', 'plaque']
        data = {field: request.form.get(field, '').strip() for field in required_fields}
        data['phone_number_2'] = request.form.get('phone_number_2', '').strip()

        if any(not data[field] for field in required_fields):
            return "خطا: لطفا تمام فیلدهای ضروری را پر کنید!"

        if not is_valid_text(data['first_name']):
            return "خطا: نام باید حداقل ۳ کاراکتر باشد!"
        if not is_valid_text(data['last_name']):
            return "خطا: نام خانوادگی باید حداقل ۳ کاراکتر باشد!"
        if not is_valid_text(data['father_name']):
            return "خطا: نام پدر باید حداقل ۳ کاراکتر باشد!"
        if not is_valid_number(data['melli_code'], 10):
            return "خطا: کد ملی باید دقیقا ۱۰ رقم عددی باشد!"
        if not is_valid_number(data['phone_number_1'], 11):
            return "خطا: شماره تماس اول باید ۱۱ رقم عددی باشد!"
        if data['phone_number_2'] and not is_valid_number(data['phone_number_2'], 11):
            return "خطا: شماره تماس دوم باید ۱۱ رقم عددی باشد!"
        if data['phone_number_2'] and data['phone_number_1'] == data['phone_number_2']:
            return "خطا: شماره تماس اول و شماره تماس دوم نباید یکسان باشند!"
        if not data['land_line'].isdigit() or not (8 <= len(data['land_line']) <= 11):
            return "خطا: تلفن ثابت باید بین ۸ تا ۱۱ رقم عددی باشد!"

        if not check_internet():
            return "خطا: اتصال اینترنت برقرار نیست! لطفا اینترنت خود را بررسی کنید."

        users.append(data)
        send_email(data)
        return "اطلاعات شما ثبت شد و ارسال گردید!"

    return render_template("index2.html", users=users)


def send_email(data):
    if not SENDER_EMAIL or not EMAIL_PASSWORD:
        print("ایمیل و پسورد تنظیم نشده است!")
        return

    receiver_email = SENDER_EMAIL
    message_content = (f"ثبت اطلاعات جدید:"
                       f"\nنام: {data['first_name']}"
                       f"\nنام خانوادگی: {data['last_name']}"
                       f"\nنام پدر: {data['father_name']}"
                       f"\nکد ملی: {data['melli_code']}"
                       f"\nشماره تماس ۱: {data['phone_number_1']}"
                       f"\nشماره تماس ۲: {data['phone_number_2'] if data['phone_number_2'] else 'ندارد'}"
                       f"\nتلفن ثابت: {data['land_line']}"
                       f"\nاستان: {data['province']}"
                       f"\nشهر: {data['city']}"
                       f"\nمحله: {data['district']}"
                       f"\nخیابان: {data['street']}"
                       f"\nکوچه: {data['alley']}"
                       f"\nپلاک: {data['plaque']}\n")

    message = MIMEText(message_content)
    message['Subject'] = 'ثبت اطلاعات جدید'
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
