import flask
from flask import request, render_template, redirect, url_for
from flask_cors import CORS
import requests


app = flask.Flask(__name__)
app.config["SECRET_KEY"] = "seasdad(*2sffcra01^23sdet"

CORS(app)

# Get this URL from the Azure Overview page of your API web app
api_url = "https://salary-api-bvbhd3d9bxegavcc.eastus-01.azurewebsites.net/"  # base url for API endpoints


# main index page route
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/predict", methods=["GET", "POST"])
def predict():
    print("in predict route")

    if request.method == "GET":
        return render_template("index.html")

    if request.method == "POST":
        print("in post method")

        form = request.form
        print("extracted form data")
        print(form)

        # Extract form data safely
        age = form.get("age")
        gender = form.get("gender")
        country = form.get("country")
        highest_deg = form.get("highest_deg")
        coding_exp = form.get("code_experience")
        title = form.get("current_title")
        company_size = form.get("company_size")

        print(age, gender, country, highest_deg, coding_exp, title, company_size)

        # Build payload for API
        salary_predict_variables = {
            "age": age,
            "gender": gender,
            "country": country,
            "highest_deg": highest_deg,
            "coding_exp": coding_exp,
            "title": title,
            "company_size": company_size,
        }

        url = f"{api_url}/predict"
        headers = {"Content-Type": "application/json"}
        print(f"Sending POST to: {url}")
        print(f"Payload: {salary_predict_variables}")

        try:
            response = requests.post(url, json=salary_predict_variables, headers=headers)

            if response.status_code == 200:
                prediction = response.json()
                print(f"Prediction response: {prediction}")
                return render_template("index.html", prediction=prediction)
            else:
                error_message = f"Failed to get prediction, status: {response.status_code}"
                print(error_message)
                return render_template("index.html", error=error_message)

        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return render_template("index.html", error="Prediction API request failed.")



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003, debug=True)
  
