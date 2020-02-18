from flask import Flask, render_template, request
from flask_httpauth import HTTPBasicAuth
import requests
import json
import os
from os import path

if path.exists(".env"):
    from dotenv import load_dotenv
    load_dotenv()

app = Flask(__name__)
auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):
    # Auth not required locally, just in production.
    # Setting an AUTH_OFF flag to any value will turn off auth.
    auth_off = os.getenv('AUTH_OFF', False)

    if auth_off:
        return True

    # If auth is on, a username and password must be supplied
    # as environment variables.
    env_username = os.environ['USERNAME']
    env_password = os.environ['PASSWORD']

    if (username == env_username) and (password == env_password):
        return True

    return False


@app.route("/")
@auth.login_required
def hello():
    return render_template('index.html')

@app.route("/results", methods=['POST'])
def submit_data():
    # Structure data to meet OpenFisca /calculate format
    data = {
        "families": {
            "_": {
                "homelessness": { "2019": request.form.get("homelessness", False) },
                "fostercare": { "2019": request.form.get("fostercare", False) },
                "eligible_tanf_or_ssi": { "2019": request.form.get("eligible_tanf_or_ssi", False) },
                "disability": { "2019": request.form.get("disability", False) },
                "household_size": { "2019": request.form["household_size"] },
                "state_or_territory": { "2019": request.form["state_or_territory"] },
                "income": { "2019": request.form["income"] },
                "head_start_eligibility_status": { "2019": None }
            }
        }
    }

    api_url = 'https://prototype-openfisca-usa-headstart.app.cloud.gov/calculate'
    api_response = requests.post(api_url, json = data)
    result = api_response.json()['families']['_']['head_start_eligibility_status']['2019']

    return render_template('results.html', result = result)

if __name__ == "__main__":
  port = int(os.getenv("PORT", 5000))
  app.run(host = '0.0.0.0', port = port)
