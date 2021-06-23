from bottle import route, get, post, run, template, debug, request, response
import dataset

# http://localhost:8080/

@route("/")
def get_todo_list():
    todo_list_db = dataset.connect('sqlite:///todo_list.db')
    todo_table = todo_list_db.get_table('todo')
    items = todo_table.find()
    items = [ dict(x) for x in list(items) ]

    return template("todo_list", items=items)

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

debug(True)
run(host="localhost", port=8080)