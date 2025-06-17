from flask import Flask, render_template, request, redirect, url_for, jsonify
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# Google Sheets – konfiguracja
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

# Endpoint do pobierania danych leadów z arkusza
@app.route("/api/sheet-leady")
def get_leady():
    try:
        sheet = client.open_by_key("1m46eTzWJTimpByqf0oNWm_LMjfwggbJNlTKw8Khrv9o").sheet1
        records = sheet.get_all_records()
        return jsonify(records)
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        login = request.form.get("login")
        password = request.form.get("password")
        if login == "admin" and password == "admin":
            return redirect(url_for("dashboard"))
        else:
            return "Błędne dane logowania"
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

if __name__ == "__main__":
    app.run(debug=True, port=5001)
