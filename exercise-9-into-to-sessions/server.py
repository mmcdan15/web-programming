from bottle import route, get, post 
from bottle import run, debug
from bottle import request, response, redirect, template
from bottle import static_file
import dataset
import json
from bottle import default_app

# http://localhost:8080/

message=None

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

@route("/login/<username>")
def get_login(username):
    global message
    message = f"Just logged in as [{username}]. Welcome!"
    response.set_cookie("username", username, path="/") #, secret='some-secret-key')
    return username

@route("/login1")
def get_login1():
    global message
    username = "santa_1"
    message = f"Just logged in as [{username}]. Welcome!"
    response.set_cookie("username", username) #, secret='some-secret-key')
    return redirect("/")

@route('/login2')
def do_login2():
    username = "santa_2"
    message = f"Just logged in as [{username}]. Welcome!"
    response.set_cookie("username", username) #, secret='some-secret-key')
    return redirect("/")

@route('/login3')
def do_login3():
    username = "santa_3"
    message = f"Just logged in as [{username}]. Welcome!"
    response.set_cookie("username", username) #, secret='some-secret-key')
    return redirect("/")

@route('/restricted')
def restricted_area():
    username = request.get_cookie("username") #, secret='some-secret-key')
    if username:
        return template("Hello {{name}}. Welcome back.", name=username)
    else:
        return "You are not logged in. Access denied."

@route("/")
def get_todo_list():
    global message
    username = request.get_cookie("username") #, secret='some-secret-key')
    print('username=',username)
    todo_list_db = dataset.connect('sqlite:///todo_list.db')
    todo_table = todo_list_db.get_table('todo')
    items = todo_table.find()
    items = [ dict(x) for x in list(items) if x['user'] == username ]
    tpl = template("todo_list", items=items, message="Logged in as " + username)
    message = None
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
