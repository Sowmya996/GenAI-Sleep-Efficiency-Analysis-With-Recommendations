from database import create_table
from flask import Flask, render_template, request
import pandas as pd
import joblib
import sqlite3


def save_report(name, gender, age, occupation,
                sleep_duration, quality_sleep,
                physical_activity, stress,
                bmi, blood_pressure,
                heart_rate, daily_steps,
                prediction):

    conn = sqlite3.connect("sleepwell.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO sleep_reports
        (
            name,
            gender,
            age,
            occupation,
            sleep_duration,
            quality_sleep,
            physical_activity,
            stress,
            bmi,
            blood_pressure,
            heart_rate,
            daily_steps,
            prediction
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        name,
        gender,
        age,
        occupation,
        sleep_duration,
        quality_sleep,
        physical_activity,
        stress,
        bmi,
        blood_pressure,
        heart_rate,
        daily_steps,
        prediction
    ))

    conn.commit()
    conn.close()
# =========================================================
# FLASK APPLICATION
# =========================================================

app = Flask(__name__)


# =========================================================
# LOAD TRAINED MACHINE LEARNING MODEL
# =========================================================

model = joblib.load("sleep_model.pkl")


# =========================================================
# HOME PAGE
# =========================================================

@app.route("/")
def home():

    return render_template("index.html")


# =========================================================
# SLEEP ASSESSMENT PAGE
# =========================================================

@app.route("/assessment")
def assessment():

    return render_template("assessment.html")


# =========================================================
# PREDICTION
# =========================================================

@app.route("/predict", methods=["POST"])
def predict():

    try:

        # =================================================
        # GET USER INPUT FROM FORM
        # =================================================
        name = request.form["name"]
        gender = request.form["gender"]

        age = int(
            request.form["age"]
        )

        occupation = request.form[
            "occupation"
        ]

        sleep_duration = float(
            request.form["sleep_duration"]
        )

        quality_sleep = int(
            request.form["quality_sleep"]
        )

        physical_activity = int(
            request.form["physical_activity"]
        )

        stress = int(
            request.form["stress"]
        )

        bmi = request.form[
            "bmi"
        ]

        blood_pressure = request.form[
            "blood_pressure"
        ]

        heart_rate = int(
            request.form["heart_rate"]
        )

        daily_steps = int(
            request.form["daily_steps"]
        )


        # =================================================
        # CREATE DATAFRAME FOR MACHINE LEARNING MODEL
        # =================================================

        user_data = pd.DataFrame(
            [
                {
                    "Gender": gender,

                    "Age": age,

                    "Occupation": occupation,

                    "Sleep Duration":
                        sleep_duration,

                    "Quality of Sleep":
                        quality_sleep,

                    "Physical Activity Level":
                        physical_activity,

                    "Stress Level":
                        stress,

                    "BMI Category":
                        bmi,

                    "Blood Pressure":
                        blood_pressure,

                    "Heart Rate":
                        heart_rate,

                    "Daily Steps":
                        daily_steps
                }
            ]
        )


        # =================================================
        # MACHINE LEARNING PREDICTION
        # =================================================
            
        print("\n==========================")
        print("User Data:")
        print(user_data)

        prediction = model.predict(user_data)[0]

        print("Prediction:", prediction)
        print("==========================\n")

        # =================================================
        # SAVE REPORT TO DATABASE
        # =================================================

        save_report(
            name,
            gender,
            age,
            occupation,
            sleep_duration,
            quality_sleep,
            physical_activity,
            stress,
            bmi,
            blood_pressure,
            heart_rate,
            daily_steps,
            prediction
        )
        # =================================================
        # PERSONALISED RECOMMENDATIONS
        # =================================================

        personal_tips = []


        # -------------------------------------------------
        # SHORT SLEEP DURATION
        # -------------------------------------------------

        if sleep_duration < 7:

            personal_tips.append(
                {
                    "icon": "⏰",

                    "title":
                        "Short Sleep Duration",

                    "message":
                        f"You reported {sleep_duration} hours "
                        "of sleep. Try to maintain a consistent "
                        "sleep schedule and allow adequate time "
                        "for sleep each night."
                }
            )


        # -------------------------------------------------
        # LONG SLEEP DURATION
        # -------------------------------------------------

        elif sleep_duration > 9:

            personal_tips.append(
                {
                    "icon": "🛏️",

                    "title":
                        "Long Sleep Duration",

                    "message":
                        f"You reported {sleep_duration} hours "
                        "of sleep. If you regularly sleep for "
                        "long periods and still feel tired, "
                        "consider discussing this with a "
                        "healthcare professional."
                }
            )


        # -------------------------------------------------
        # HIGH STRESS
        # -------------------------------------------------

        if stress >= 7:

            personal_tips.append(
                {
                    "icon": "🧘",

                    "title":
                        "High Stress Level",

                    "message":
                        f"Your reported stress level is "
                        f"{stress}/10. Consider relaxation "
                        "techniques such as slow breathing, "
                        "meditation, gentle stretching or a "
                        "calming bedtime routine."
                }
            )


        # -------------------------------------------------
        # LOW SLEEP QUALITY
        # -------------------------------------------------

        if quality_sleep <= 5:

            personal_tips.append(
                {
                    "icon": "🌙",

                    "title":
                        "Low Sleep Quality",

                    "message":
                        f"You rated your sleep quality "
                        f"{quality_sleep}/10. Try maintaining "
                        "a regular sleep schedule and keeping "
                        "your bedroom quiet, comfortable and "
                        "suitable for sleeping."
                }
            )


        # -------------------------------------------------
        # MODERATE SLEEP QUALITY
        # -------------------------------------------------

        elif quality_sleep <= 7:

            personal_tips.append(
                {
                    "icon": "💤",

                    "title":
                        "Improve Sleep Quality",

                    "message":
                        f"Your reported sleep quality is "
                        f"{quality_sleep}/10. A consistent "
                        "bedtime routine and reduced stimulation "
                        "before bed may help support better sleep."
                }
            )


        # -------------------------------------------------
        # LOW PHYSICAL ACTIVITY
        # -------------------------------------------------

        if physical_activity < 40:

            personal_tips.append(
                {
                    "icon": "🏃",

                    "title":
                        "Increase Daytime Activity",

                    "message":
                        "Your reported physical activity level "
                        "is relatively low. Appropriate regular "
                        "daytime activity may support overall "
                        "health and sleep."
                }
            )


        # -------------------------------------------------
        # LOW DAILY STEPS
        # -------------------------------------------------

        if daily_steps < 5000:

            personal_tips.append(
                {
                    "icon": "🚶",

                    "title":
                        "More Daily Movement",

                    "message":
                        f"You reported approximately "
                        f"{daily_steps} steps per day. "
                        "If appropriate for you, gradually "
                        "adding more everyday movement can "
                        "support overall health."
                }
            )


        # -------------------------------------------------
        # MODERATE DAILY STEPS
        # -------------------------------------------------

        elif daily_steps < 7500:

            personal_tips.append(
                {
                    "icon": "👟",

                    "title":
                        "Keep Moving",

                    "message":
                        f"You reported approximately "
                        f"{daily_steps} steps per day. "
                        "Continue incorporating regular "
                        "movement throughout your day."
                }
            )


        # -------------------------------------------------
        # POSITIVE SLEEP HABITS
        # -------------------------------------------------

        if (
            sleep_duration >= 7
            and sleep_duration <= 9
            and quality_sleep >= 7
            and stress <= 5
        ):

            personal_tips.append(
                {
                    "icon": "✨",

                    "title":
                        "Positive Sleep Habits",

                    "message":
                        "Several of your reported sleep factors "
                        "look favourable. Continue maintaining "
                        "a consistent sleep schedule and healthy "
                        "daytime routine."
                }
            )


        # =================================================
        # CONDITION-SPECIFIC RECOMMENDATION
        # =================================================


        # INSOMNIA
        if prediction == "Insomnia":

            personal_tips.append(
                {
                    "icon": "🌙",

                    "title":
                        "Insomnia Support",

                    "message":
                        "Your sleep pattern resembles patterns "
                        "associated with insomnia in our model. "
                        "If difficulty falling asleep or staying "
                        "asleep continues and affects daily life, "
                        "consider speaking with a qualified "
                        "healthcare professional."
                }
            )


        # SLEEP APNEA
        elif prediction == "Sleep Apnea":

            personal_tips.append(
                {
                    "icon": "🫁",

                    "title":
                        "Sleep Apnea Evaluation",

                    "message":
                        "Your sleep pattern resembles patterns "
                        "associated with sleep apnea in our model. "
                        "If you experience loud snoring, breathing "
                        "pauses, choking during sleep or excessive "
                        "daytime sleepiness, consider professional "
                        "medical evaluation."
                }
            )


        # HEALTHY
        elif prediction == "Healthy":

            personal_tips.append(
                {
                    "icon": "💚",

                    "title":
                        "Maintain Healthy Habits",

                    "message":
                        "Your information resembles the healthy "
                        "sleep patterns represented in our model. "
                        "Continue maintaining healthy sleep, "
                        "activity and lifestyle habits."
                }
            )


        # =================================================
        # SEND RESULT TO RESULT.HTML
        # =================================================

        return render_template(

            "result.html",

            prediction=prediction,

            sleep_duration=sleep_duration,

            quality_sleep=quality_sleep,

            stress=stress,

            physical_activity=physical_activity,

            daily_steps=daily_steps,

            personal_tips=personal_tips
        )


    # =====================================================
    # ERROR HANDLING
    # =====================================================

    except Exception as error:

        return f"""

        <html>

        <head>

            <title>
                SleepWell Error
            </title>

        </head>


        <body style="
            background:#071126;
            color:white;
            font-family:Arial;
            text-align:center;
            padding-top:100px;
        ">


            <h1>
                🌙 SleepWell
            </h1>


            <h2>
                Something went wrong
            </h2>


            <p style="
                color:#ffb4b4;
            ">

                {error}

            </p>


            <br>


            <a
                href="/assessment"

                style="
                    background:#7695ff;
                    color:white;
                    padding:14px 24px;
                    text-decoration:none;
                    border-radius:10px;
                "
            >

                ← Return to Assessment

            </a>


        </body>

        </html>

        """


# =========================================================
# START FLASK SERVER
# =========================================================
create_table()
if __name__ == "__main__":

    app.run(
        debug=True
    )
#Displaying app.py.