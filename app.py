from flask_cors import CORS
from user_agents import parse 
from flask import Flask, render_template, request, redirect, url_for, session
from datetime import timedelta
from functools import wraps
from waitress import serve

app = Flask(__name__)
CORS(app)  
app.secret_key = 'sua_chave_secreta' 
app.permanent_session_lifetime = timedelta(minutes=60)  

@app.context_processor
def inject_static_url():
    # Adiciona o URL estático a todos os templates
    return dict(static_url=url_for('static', filename=''))

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Redireciona para a página de login se o usuário não estiver autenticado
        if "user" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    # Determina a versão da página a ser renderizada com base no tipo de dispositivo
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
    # Renderiza a página de checkout apropriada para cada tipo de dispositivo
    if user_agent.is_pc:
        return render_template('LandingPage_Checkout_Desktop.html')
    elif user_agent.is_mobile:
        return render_template('LandingPage_Checkout_Mobile.html')

@app.route('/plan/studio/checkout')
def plan_studio_checkout():
    ua_string = request.headers.get('User-Agent')
    user_agent = parse(ua_string)
    # Renderiza a página de checkout apropriada para cada tipo de dispositivo
    if user_agent.is_pc:
        return render_template('LandingPage_Checkout_Desktop.html')
    elif user_agent.is_mobile:
        return render_template('LandingPage_Checkout_Mobile.html')

@app.route("/checkout/sucess", methods=["GET", "POST"])
def checkout_sucess():
    ua_string = request.headers.get('User-Agent')
    user_agent = parse(ua_string)
    # Renderiza a página de sucesso de checkout para cada tipo de dispositivo
    if user_agent.is_pc:
        return render_template('LandingPage_Checkout_Desktop_Sucess_Page.html')
    elif user_agent.is_mobile:
        return render_template('LandingPage_Checkout_Mobile_Sucess_Page.html')

@app.route("/checkout/cancel", methods=["GET", "POST"])
def checkout_cancel():
    ua_string = request.headers.get('User-Agent')
    user_agent = parse(ua_string)
    # Renderiza a página de cancelamento de checkout para cada tipo de dispositivo
    if user_agent.is_pc:
        return render_template('LandingPage_Checkout_Desktop_Cancel_Page.html')
    elif user_agent.is_mobile:
        return render_template('LandingPage_Checkout_Mobile_Cancel_Page.html')

# Quando você estiver pronto para implantar a aplicação, descomente a linha abaixo
# if __name__ == '__main__':
#     serve(app, host="0.0.0.0", port=800)
