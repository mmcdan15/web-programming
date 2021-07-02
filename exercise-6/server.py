from bottle import route, get, post, run, template, debug, request, response, redirect
import dataset
import json
from bottle import default_app

# http://localhost:8080/

@route("/")
def get_todo_list():
    todo_list_db = dataset.connect('sqlite:///todo_list.db')
    todo_table = todo_list_db.get_table('todo')
    items = todo_table.find()
    items = [ dict(x) for x in list(items) ]

    return template("todo_list", items=items)

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
    return template("inserted")

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
