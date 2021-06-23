from bottle import route, run, template, debug
import dataset

# http://localhost:8068/

@route("/")
def get_todo_list():

    todo_list_db = dataset.connect('sqlite:///todo_list.db')
    todo_table = todo_list_db.get_table('todo')
    items = todo_table.find()
    items = [ dict(x) for x in list(items) ]

    return template("todo_list", items=items)

debug(True)
run(host="localhost", port=8080)