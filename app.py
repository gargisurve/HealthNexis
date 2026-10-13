from flask import Flask, request, jsonify, send_file, render_template
from flask_cors import CORS
from lifestyle_model import train_model
import mysql.connector
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
import pandas as pd

app = Flask(__name__)
CORS(app)

# ==========================
# LOAD MODEL
# ==========================
model = train_model()

# ==========================
# DB CONNECTION
# ==========================
db = mysql.connector.connect(
    host="localhost",
    user="db_user_name",
    password="db_password",
    database="lifestyle_disease"
)

# ==========================
# RISK CATEGORY
# ==========================
def get_risk_category(risk):
    if risk < 30:
        return "Low"
    elif risk < 60:
        return "Moderate"
    else:
        return "High"


# ==========================
# CLEAN TOP DRIVERS
# ==========================
def get_top_drivers():
    try:
        clf = model.named_steps['classifier']
        coefs = clf.coef_[0]
        feature_names = model.named_steps['preprocessing'].get_feature_names_out()

        impacts = []
        for name, coef in zip(feature_names, coefs):
            impacts.append((name, abs(coef)))

        impacts.sort(key=lambda x: x[1], reverse=True)
        top3 = impacts[:3]

        cleaned = []
        for name, _ in top3:
            name = name.replace("num__", "").replace("cat__", "")

            if "_" in name:
                parts = name.split("_", 1)
                readable = f"{parts[0]}: {parts[1]}"
            else:
                readable = name

            cleaned.append(readable)

        return cleaned
    except:
        return []


# ==========================
# ROOT
# ==========================
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/admin")
def admin():
    return render_template("admin.html")

@app.route("/index")
def index():
    return render_template("index.html")


# ==========================
# PREDICT
# ==========================
@app.route("/predict", methods=["POST"])
def predict():

    data = request.json

    input_df = pd.DataFrame([{
        "Age": data["Age"],
        "Height(cm)": data["Height"],
        "Weight(kg)": data["Weight"],
        "SleepHours": data["SleepHours"],
        "StressLevel": data["StressLevel"],
        "BMI": data["BMI"],
        "Gender": data["Gender"],
        "Occupation": data["Occupation"],
        "Diet": data["Diet"],
        "JunkFood": data["JunkFood"],
        "Smoking": data["Smoking"],
        "Alcohol": data["Alcohol"],
        "FamilyHistory": data["FamilyHistory"]
    }])

    prediction = model.predict(input_df)[0]
    probability = model.predict_proba(input_df)[0][1] * 100

    category = get_risk_category(probability)
    drivers = get_top_drivers()

    cursor = db.cursor()

    # Population comparison
    cursor.execute("SELECT AVG(risk) FROM predictions")
    avg_population = cursor.fetchone()[0]

    if avg_population is None:
        percentile_msg = "Not enough population data"
    else:
        if probability > avg_population:
            percentile_msg = "Above population average risk"
        else:
            percentile_msg = "Below population average risk"

    # Insert into DB (NOW INCLUDING CATEGORY)
    cursor.execute("""
        INSERT INTO predictions
        (age,height,weight,sleep,stress,bmi,gender,occupation,diet,junkfood,
         smoking,alcohol,family_history,risk,category,created_at)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
        data["Age"], data["Height"], data["Weight"],
        data["SleepHours"], data["StressLevel"], data["BMI"],
        data["Gender"], data["Occupation"], data["Diet"],
        data["JunkFood"], data["Smoking"], data["Alcohol"],
        data["FamilyHistory"],
        float(probability),
        category,
        datetime.now()
    ))

    db.commit()
    prediction_id = cursor.lastrowid

    return jsonify({
        "risk": round(probability, 2),
        "category": category,
        "drivers": drivers,
        "population_comparison": percentile_msg,
        "prediction_id": prediction_id
    })


# ==========================
# HISTORY
# ==========================
@app.route("/history")
def history():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT id, risk, created_at FROM predictions ORDER BY id")
    return jsonify(cursor.fetchall())


# ==========================
# ANALYTICS
# ==========================
@app.route("/analytics")
def analytics():
    cursor = db.cursor()

    cursor.execute("SELECT COUNT(*) FROM predictions")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT AVG(risk) FROM predictions")
    avg = cursor.fetchone()[0]

    cursor.execute("""
        SELECT 
            SUM(CASE WHEN risk < 30 THEN 1 ELSE 0 END),
            SUM(CASE WHEN risk BETWEEN 30 AND 60 THEN 1 ELSE 0 END),
            SUM(CASE WHEN risk > 60 THEN 1 ELSE 0 END)
        FROM predictions
    """)
    dist = cursor.fetchone()

    return jsonify({
        "total_users": total,
        "average_risk": round(avg,2) if avg else 0,
        "distribution": {
            "low": dist[0] or 0,
            "moderate": dist[1] or 0,
            "high": dist[2] or 0
        }
    })


# ==========================
# DETAILED PDF REPORT
# ==========================
@app.route("/report/<int:prediction_id>")
def generate_report(prediction_id):

    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM predictions WHERE id=%s", (prediction_id,))
    record = cursor.fetchone()

    if not record:
        return "Record not found"

    filename = f"report_{prediction_id}.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    # TITLE
    elements.append(Paragraph("<b>AI Lifestyle Disease Risk Assessment Report</b>", styles['Title']))
    elements.append(Spacer(1, 20))

    # RISK OVERVIEW
    elements.append(Paragraph(f"<b>Risk Score:</b> {record['risk']}%", styles['Normal']))
    elements.append(Paragraph(f"<b>Risk Category:</b> {record['category']}", styles['Normal']))
    elements.append(Spacer(1, 12))

    # USER INPUT SUMMARY
    elements.append(Paragraph("<b>User Input Summary:</b>", styles['Heading2']))
    elements.append(Spacer(1, 8))

    elements.append(Paragraph(f"Age: {record['age']}", styles['Normal']))
    elements.append(Paragraph(f"BMI: {record['bmi']}", styles['Normal']))
    elements.append(Paragraph(f"Sleep Hours: {record['sleep']}", styles['Normal']))
    elements.append(Paragraph(f"Stress Level: {record['stress']}", styles['Normal']))
    elements.append(Paragraph(f"Smoking: {record['smoking']}", styles['Normal']))
    elements.append(Paragraph(f"Alcohol: {record['alcohol']}", styles['Normal']))
    elements.append(Spacer(1, 12))

    # RECOMMENDATION
    elements.append(Paragraph("<b>AI Recommendation:</b>", styles['Heading2']))
    elements.append(Spacer(1, 8))

    if record['risk'] < 30:
        recommendation = "Maintain your current lifestyle and healthy habits."
    elif record['risk'] < 60:
        recommendation = "Moderate risk detected. Improve diet, sleep and stress management."
    else:
        recommendation = "High risk detected. Immediate lifestyle modification and medical consultation recommended."

    elements.append(Paragraph(recommendation, styles['Normal']))
    elements.append(Spacer(1, 20))

    # FOOTER
    elements.append(Paragraph(
        "Generated by Cloud-Integrated Lifestyle Disease Risk Prediction System",
        styles['Italic']
    ))
    elements.append(Paragraph(
        f"Generated on: {record['created_at']}",
        styles['Normal']
    ))

    doc.build(elements)

    return send_file(filename, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=False)
