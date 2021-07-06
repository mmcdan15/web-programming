from bottle import route, run, template

# http://localhost:8068/

@route("/")
def get_index():
    return "Hello!"

run(host="localhost", port=8068)