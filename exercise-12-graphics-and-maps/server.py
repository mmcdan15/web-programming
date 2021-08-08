from bottle import route, get, post 
from bottle import run, debug
from bottle import request, response, redirect, template
from bottle import static_file
import dataset
import json
from bottle import default_app
import random
import string
import hashlib
import os
import codecs
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def bytes_to_str(b):
    s = str(codecs.encode(b,"hex"),"utf-8")
    assert type(s) is str
    return s

def str_to_bytes(s):
    b = codecs.decode(bytes(s,"utf-8"),"hex")
    assert type(b) is bytes
    return b

def generate_credentials(password):
    salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac(
        'sha256', # The hash digest algorithm for HMAC
        password.encode('utf-8'), # Convert the password to bytes
        salt, # Provide the salt
        100000 # It is recommended to use at least 100,000 iterations of SHA-256 
        )
    print(salt)
    print(key)
    return {
        'salt':bytes_to_str(salt), 
        'key' :bytes_to_str(key),
    }

def verify_password(password, credentials):
    salt = str_to_bytes(credentials['salt'])
    key  = str_to_bytes(credentials['key'])
    print(salt)
    print(key)
    new_key = hashlib.pbkdf2_hmac(
        'sha256', # The hash digest algorithm for HMAC
        password.encode('utf-8'), # Convert the password to bytes
        salt, # Provide the salt
        100000 # It is recommended to use at least 100,000 iterations of SHA-256 
        )
    return new_key == key

def write(key, data):
    assert type(data) is dict
    with open(f"data/session.{key}.json", "w") as f:
        json.dump(data,f)
    return

def read(key):
    with open(f"data/session.{key}.json", "r") as f:
        data = json.load(f)
    assert type(data) is dict
    return data

def create_token(k=32):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=k))

def new_session_id():
    return create_token()

def get_session(request):
    
    def new_session():
        session_id = new_session_id()
        print("new session id = ", session_id)
        session = {
            "session_id" : session_id,
            "username" : ''
        }
        return session

    session_id = request.get_cookie("session_id", default=None)
    if session_id == None:
        session = new_session()
    else:
        try:
            session = read(session_id)
        except: 
            session = new_session()
    print("loaded session = ", [session])
    return session

def save_session(response, session):
    # session =  [{'session_id': 'khlrry5slw5d5fmlawvrfz8oqz7tl8ue', 'username': ''}]
    write(session['session_id'], session)
    print("saved session = ",[session])
    response.set_cookie("session_id", session['session_id'], path="/") #, secret='some-secret-key')

def get_user(name):
    try:
        with open(f"data/user.{name}.json", "r") as f:
            data = json.load(f)
        assert type(data) is dict
        return data
    except:
        return None

def save_user(name, data):
    assert type(data) is dict
    with open(f"data/user.{name}.json", "w") as f:
        json.dump(data,f)
    return
    print("saved user = ",[name])

@route("/table")
def get_table():
    table = [
        {'a':1, 'b':'alpha'},
        {'a':2, 'b':'beta'},
    ]
    return template('table',table=table)

@route("/drawing")
def get_drawing():
    return template('drawing')

@route("/chart")
def get_drawing():
    return template('chart')

@route("/request")
def get_request():
    environ = request.environ
    table = [ {"key":key,"value":environ[key]} for key in environ.keys()]
    return template('table',table=table)

@get("/login")
def get_login():
    return template("login")

@post("/login")
def post_login():
    session = get_session(request)
    username = request.forms.get('username')
    password = request.forms.get('password')
    user = get_user(username)
    if not user:
        print("no such user")
        return redirect('/signup')
    if 'credentials' not in user:
        print("credentials missing")
        return redirect('/signup')
    if not verify_password(password, user['credentials']):
        print('failed verification')
        return redirect('/')
    print("successful login")
    session['username'] = username
    save_session(response, session)
    return redirect('/')

def send_verification_email(username):
    user = get_user(username)
    if not user:
        print("failure to find user")
        return
    print(user)
    email = user['email']
    token = create_token()
    user['token'] = token
    save_user(username, user)
    print('user information with token has been saved')

    verify_url = f"http://localhost:8080/verify/{token}"

    # send_message(email, message)
    sender = "<app@example.com>"
    receiver = f"{username}<{email}>"

    text = f"""\
        Please verify your email by visiting this page in your browser. 
        
        {verify_url}

        Thanks! 

        The admins..
    """

    html = f"""\
        <html>
        <body>
        <p>Please verify your email by clicking here.<br/></p>

        <p><a href="{verify_url}">{verify_url}</a><br/></p>

        <p>-Thanks!<br>The admins/></p>
        </body>
        </html>
    """

    message = MIMEMultipart("alternative")
    message["Subject"] = "Please verify your email"
    message["From"] = sender
    message["To"] = receiver

    message.attach(MIMEText(text,"plain"))
    message.attach(MIMEText(html,"html"))

    with smtplib.SMTP("smtp.mailtrap.io", 2525) as server:
        server.login("4e83cff9aba69f", "988d5260c1b156")
        server.sendmail(sender, receiver, message.as_string())

    return

def send_reset_email(username):
    user = get_user(username)
    if not user:
        print("failure to find user")
        return
    print(user)
    email = user['email']
    token = create_token()
    user['reset_token'] = token
    save_user(username, user)
    print('user information with reset token has been saved')

    reset_url = f"http://localhost:8080/reset/{username}/{token}"

    # send_message(email, message)
    sender = "<app@example.com>"
    receiver = f"{username}<{email}>"

    text = f"""\
        Please reset your password by visiting this page in your browser. 
        
        {reset_url}

        Thanks! 

        The admins..
    """

    html = f"""\
        <html>
        <body>
        <p>Please verify your email by clicking here.<br/></p>

        <p><a href="{reset_url}">{reset_url}</a><br/></p>

        <p>-Thanks!<br>The admins/></p>
        </body>
        </html>
    """

    message = MIMEMultipart("alternative")
    message["Subject"] = "Password reset request"
    message["From"] = sender
    message["To"] = receiver

    message.attach(MIMEText(text,"plain"))
    message.attach(MIMEText(html,"html"))

    with smtplib.SMTP("smtp.mailtrap.io", 2525) as server:
        server.login("4e83cff9aba69f", "988d5260c1b156")
        server.sendmail(sender, receiver, message.as_string())

    return

@get("/signup")
def get_signup():
    return template("signup")

@post("/signup")
def post_signup():
    session = get_session(request)
    username = request.forms.get('username')
    password = request.forms.get('password')
    password_again = request.forms.get('password_again')
    email = request.forms.get('email')
    if password != password_again:
        #TODO: suitable message in session
        save_session(response, session)
        return redirect('/')    
    save_user(username, {
        'username':username,
        'credentials':generate_credentials(password),
        'email':email,
        'email_verified':False
    })
    send_verification_email(username)
    session['username'] = username
    #TODO: suitable message in session
    save_session(response, session)
    return redirect('/')

@get("/verify/<token>")
def get_verify(token):
    session = get_session(request)
    username = session['username']
    user = get_user(username)
    print(token)
    print(user)
    if token == user['token']:
        user['email_verified'] = True
        save_user(username, user)

@get("/forgot")
def get_signup():
    return template("forgot")

@post("/forgot")
def post_signup():
    session = get_session(request)
    username = request.forms.get('username')
    user = get_user(username)
    if user['email_verified']:
        send_reset_email(username)
    return redirect('/')

@get("/reset/<username>/<reset_token>")
def get_reset(username, reset_token):
    session = get_session(request)
    session['csrf_token'] = create_token()
    user = get_user(username)
    print(reset_token)
    print(user)
    if reset_token == user['reset_token']:
        save_session(response, session)
        return template("reset", username=username, reset_token=reset_token, csrf_token=session['csrf_token'])
    return redirect('/')

@post("/reset/<username>/<reset_token>")
def post_reset(username, reset_token):
    session = get_session(request)
    if 'csrf_token' not in session:
        redirect('/')
    # check the csrf token
    if request.forms.get('csrf_token') != session['csrf_token']:
        redirect('/')
    session['csrf_token'] = None
    user = get_user(username)
    print(reset_token)
    print(user)
    if reset_token != user['reset_token']:
        return redirect('/')
    user['reset_token'] = None
    # get new password
    password = request.forms.get('password')
    password_again = request.forms.get('password_again')
    if password != password_again:
        #TODO: suitable message in session
        save_session(response, session)
        return redirect('/') 
    user['credentials'] == generate_credentials(password)  
    save_user(username, user)
    return redirect('/login')

@get("/logout")
def get_logout():
    session = get_session(request)
    session['username'] = ''
    save_session(response, session)
    return redirect('/')

@route('/restricted')
def restricted_area():
    username = request.get_cookie("username") #, secret='some-secret-key')
    if username:
        return template("Hello {{name}}. Welcome back.", name=username)
    else:
        return "You are not logged in. Access denied."

@route("/")
def get_todo_list():
    session = get_session(request)
    print("session = ", [session])
    username = session['username']
    todo_list_db = dataset.connect('sqlite:///todo_list.db')
    todo_table = todo_list_db.get_table('todo')
    items = todo_table.find()
    items = [ dict(x) for x in list(items) if x['user'] == username ]
    tpl = template("todo_list", items=items, message="Logged in as " + username, status=None)
    save_session(response, session)
    return tpl

@route("/data")
def get_data():
    pets = [
    {
        "name": "Dorothy",
        "kind": "dog",
    },
    {
        "name": "Squeakers",
        "kind": "guinea pig",
    },
    {
        "name": "Sandy",
        "kind": "cat",
    }
    ]
    
    response.content_type = 'application/json'
    return json.dumps({"pets":pets})

@route("/static/png/<filename:re:.*\.png>")
@route("/image/<filename:re:.*\.png>")
def get_image(filename):
    return static_file(filename=filename, root="static/images", mimetype="image/png")

@route("/static/<filename:path>")
def get_static(filename):
    return static_file(filename=filename, root="static")

@route("/show")
def get_show():
    return template("show")

@route('/counter')
def get_counter():
    count = int(request.get_cookie("count", default='0', secret="Elephant12"))
    count = count + 1
    response.set_cookie("count", str(count), secret="Elephant12")
    return template("counter", count=count)

@route("/delete/<id>")
def get_delete(id):
    id = int(id)
    try:
        todo_list_db = dataset.connect('sqlite:///todo_list.db')
        todo_table = todo_list_db.get_table('todo')
        print(f"We need to delete id# {id}...")
        todo_table.delete(id=id)
    except Exception as e:
        response.status="409 Bad Request:"+str(e)
        return
    return template("deleted", id=id)

@get("/insert")
def get_insert():
    global message
    message = "A task was added"
    return template("insert")

@post("/insert")
def post_insert():
    task = request.forms.get('task')
    print("task=", task)
    try:
        todo_list_db = dataset.connect('sqlite:///todo_list.db')
        todo_table = todo_list_db.get_table('todo')
        todo_table.insert({
            'task' : task.strip(),
            'done' : 0
        })
    except Exception as e:
        response.status="409 Bad Request:"+str(e)
        return
    return redirect('/')

@get("/edit/<id>")
def get_edit(id):
    try:
        todo_list_db = dataset.connect('sqlite:///todo_list.db')
        todo_table = todo_list_db.get_table('todo')
        items = list(todo_table.find(id=id))
        if len(items) != 1:
            response.status="404 Not Found:"+str(id)
            return
        items = [ dict(x) for x in items ]
        print(items)
        print(items[0])
    except Exception as e:
        print(e)
        response.status="409 Bad Request:"+str(e)
        return

    return template("edit", item=items[0])  # put something here

@post("/edit")
def post_edit():
    id = request.forms.get('id')
    id = int(id)
    task = request.forms.get('task')
    print("task=", task)
    try:
        todo_list_db = dataset.connect('sqlite:///todo_list.db')
        todo_table = todo_list_db.get_table('todo')
        todo_table.update({
            'id' : id,
            'task' : task.strip(),
        }, ['id'])
    except Exception as e:
        response.status="409 Bad Request:"+str(e)
        return
    return redirect('/')

if __name__ == "__main__":
    debug(True)
    run(host="localhost", port=8080)
else:
    application = default_app()
