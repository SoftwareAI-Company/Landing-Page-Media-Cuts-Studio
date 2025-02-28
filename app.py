from flask_cors import CORS
from user_agents import parse 
from flask import Flask, render_template, request, redirect, url_for, session
from datetime import timedelta
from functools import wraps


app = Flask(__name__)
CORS(app)  
app.secret_key = 'sua_chave_secreta' 
app.permanent_session_lifetime = timedelta(minutes=60)  

@app.context_processor
def inject_static_url():
    return dict(static_url=url_for('static', filename=''))

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    ua_string = request.headers.get('User-Agent')
    user_agent = parse(ua_string)
    if user_agent.is_tablet:
        return render_template('LandingPage_Tablet.html')
    elif user_agent.is_mobile:
        return render_template('LandingPage_Mobile.html')
    else:
        return render_template('LandingPage_Desktop.html')

@app.route('/plan/content-creator/checkout')
def plan_contentcreator_checkout():
    ua_string = request.headers.get('User-Agent')
    user_agent = parse(ua_string)
    if user_agent.is_pc:
        return render_template('LandingPage_Checkout_Desktop.html')
    elif user_agent.is_mobile:
        return render_template('LandingPage_Checkout_Mobile.html')

@app.route('/plan/studio/checkout')
def plan_studio_checkout():
    ua_string = request.headers.get('User-Agent')
    user_agent = parse(ua_string)
    if user_agent.is_pc:
        return render_template('LandingPage_Checkout_Desktop.html')
    elif user_agent.is_mobile:
        return render_template('LandingPage_Checkout_Mobile.html')

@app.route("/checkout/sucess", methods=["GET", "POST"])
def checkout_sucess():
    ua_string = request.headers.get('User-Agent')
    user_agent = parse(ua_string)
    if user_agent.is_pc:
        return render_template('LandingPage_Checkout_Desktop_Sucess_Page.html')
    elif user_agent.is_mobile:
        return render_template('LandingPage_Checkout_Mobile_Sucess_Page.html')

@app.route("/checkout/cancel", methods=["GET", "POST"])
def checkout_cancel():
    ua_string = request.headers.get('User-Agent')
    user_agent = parse(ua_string)
    if user_agent.is_pc:
        return render_template('LandingPage_Checkout_Desktop_Cancel_Page.html')
    elif user_agent.is_mobile:
        return render_template('LandingPage_Checkout_Mobile_Cancel_Page.html')







if __name__ == '__main__':
    app.run(debug=True, port=800)
