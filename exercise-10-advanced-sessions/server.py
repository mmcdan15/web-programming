from bottle import route, get, post 
from bottle import run, debug
from bottle import request, response, redirect, template
from bottle import static_file
import dataset
import json
from bottle import default_app
import random
import string

# http://localhost:8080/

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

def new_session_id():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=32))

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

@route("/table")
def get_table():
    table = [
        {'a':1, 'b':'alpha'},
        {'a':2, 'b':'beta'},
    ]
    return template('table',table=table)

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
    session['username'] = username
    save_session(response, session)
    return redirect('/')

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
    tpl = template("todo_list", items=items, message="Logged in as " + username)
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
