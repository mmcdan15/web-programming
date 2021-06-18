from bottle import route, run, template, debug

# http://localhost:8068/

@route("/")
def get_index():
    return "Hello!"

@route("/hello")
@route("/hello/<name>")
def get_hello(name="Santa"):
    data = {
        "holiday":False,
        'people':[
            {
                "name":"Santa",
                "title":"Mr"
            },
            {
                "name":"Wendy",
                "title":"Ms."
            },
            {
                "name":"Greg",
                "title":"Dr."
            }
        ],
    }
    name = "Santa"
    return template("hello", data=data)

debug(True)
run(host="localhost", port=8068)