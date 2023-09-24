# Write a web app that allows user to submit a form.

# Clarifying Questions:
# Should we focus on the function or do we need to style the form?
# What is the function of this webpage?
# What are the fields of the form?
# What validations do we need for each field? Client-side or server-side
# What should we return after submitting the form?
# """

##########################################################################################

from flask import Flask, request, redirect, url_for, render_template, jsonify
import uuid 
import re
import requests

users = {
    "1" : {
        "name" : "elroy",
        "address" : "80 Pasir Panjang, Singapore 686680",
        "contact" : 99999999
    },
    "2" : {
        "name" : "marc",
        "address" : "70 Pasir Panjang, Singapore 686670",
        "contact" : 91234567
    }
}

def validate_address(address):
    components = address.split(",")
    return len(components) >= 3
    # API_KEY = ""
    # url = f"https://addressvalidation.googleapis.com/v1:validateAddress?key={API_KEY}"
    # headers = {
    #     'Content-Type' : "application/json"
    # }
    # body = {
    #     "address" : {
    #         "addressLines" : [address],
    #     }
    # }
    # response = requests.post(url, headers=headers, json=body)
    # try:
    #     # Check response and validate
    #     confirmList  = [x["confirmationLevel"] for x in response["result"]["address"]["addressComponents"]]
    #     for x in confirmList:
    #         if x != "CONFIRMED":
    #             return False
    #         else:
    #             return True
    # except:
    #     return False

def validate_contact(contact):
    contact_pattern = r'^[689]\d{7}'
    return re.match(contact_pattern, contact)

##########################################################################################

app = Flask(__name__)

@app.route("/")
def form():
    error = request.args.get("error", "")
    return render_template("index.html", error=error)

@app.route("/submit_form", methods=["POST"])
def submit():
    name = request.form.get("name")
    address = request.form.get("address")
    contact = request.form.get("contact")

    if not validate_address(address):
        error = "400: Invalid Address Format!"
        return redirect(url_for("form", error=error))
    if not validate_contact(contact):
        error = "400: Invalid Contact Format!"
        return redirect(url_for("form", error=error))

    user_id = str(uuid.uuid4())
    user = {
        "name" : name,
        "address" : address,
        "contact" : contact
    }

    print(users)
    users[user_id] = user

    return redirect(url_for("home", name=name, address=address, contact=contact))

@app.route("/home")
def home():
    name = request.args.get("name")
    address = request.args.get("address")
    contact = request.args.get("contact")

    return render_template("home.html", name=name, address=address, contact=contact)    

@app.route("/users")
def list_users():
    return render_template("users.html", users=users)

@app.route("/user/<int:user_id>", methods=["GET", "PUT", "DELETE"])
def user(user_id):
    if request.method == "GET":
        try:
            if user_id in users:
                user = users[user_id]
                return jsonify(user)
            else:
                return {"error": "User not found!"}, 404
        except KeyError as e:
            return str(e), 400
        except Exception as e:
            return str(e), 500
    
    if request.method == "PUT":
        try:
            if user_id in users:
                name = request.args.get("name", users[user_id]['name'])
                address = request.args.get("address", users[user_id]['address'])
                contact = request.args.get("contact", users[user_id]['contact'])
                if address and not validate_address(address):
                    error = "400: Invalid Address Format!"
                    return redirect(url_for("form", error=error))
                if contact and not validate_contact(contact):
                    error = "400: Invalid Contact Format!"
                    return redirect(url_for("form", error=error))
                users[user_id] = {
                    "name" : name,
                    "address" : address,
                    "contact" : contact
                }
                return "", 204
            else:
                return {"error": "User not found!"}, 404
        except KeyError as e:
            return str(e), 400
        except Exception as e:
            return str(e), 500

    if request.method == "DELETE":
        try:
            if user_id in users:
                del users[user_id]
                return "", 204
            else:
                return {"error": "User not found!"}, 404
        except KeyError as e:
            return str(e), 400
        except Exception as e:
            return str(e), 500

if __name__ == "__main__":
    app.run()

# """