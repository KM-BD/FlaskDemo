from flask import Flask, request, render_template_string, redirect, url_for

app = Flask(__name__)

# Home page with the password form
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        password = request.form['password']
        if not check_password(password):
            return render_template_string(home_page, error="Password does not meet the requirements")
        return redirect(url_for('welcome', password=password))
    return render_template_string(home_page)

# Welcome page
@app.route('/welcome')
def welcome():
    password = request.args.get('password', '')
    return render_template_string(welcome_page, password=password)

# Password checking function
def check_password(password):
    if len(password) < 8:
        return False
    if password in common_passwords:
        return False
    return True

# Load common passwords
with open('10-million-password-list-top-1000.txt') as f:
    common_passwords = set(f.read().splitlines())

# HTML templates
home_page = '''
<!doctype html>
<html>
<head><title>Home</title></head>
<body>
    <h1>Enter your password</h1>
    <form method="post">
        <input type="password" name="password" required>
        <input type="submit" value="Login">
    </form>
    {% if error %}
    <p style="color:red;">{{ error }}</p>
    {% endif %}
</body>
</html>
'''

welcome_page = '''
<!doctype html>
<html>
<head><title>Welcome</title></head>
<body>
    <h1>Welcome!</h1>
    <p>Your password is: {{ password }}</p>
    <form action="/">
        <input type="submit" value="Logout">
    </form>
</body>
</html>
'''

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
