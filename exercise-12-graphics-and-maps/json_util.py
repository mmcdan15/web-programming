import json
import random
import string

def write(key, data):
    assert type(data) is dict
    with open(f"data/{key}.json", "w") as f:
        json.dump(data,f)
    return

def read(key):
    with open(f"data/{key}.json", "r") as f:
        data = json.load(f)
    assert type(data) is dict
    return data

def session_id():
    id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=32))
    return str(id)

def test_write_and_read():
    data = {
        "name":"dorothy",
        "kind":"dog",
        "age":4
    }
    key = "83450985adfa"
    write(key, data)
    new_data = read(key)
    assert new_data["name"] == "dorothy"
    assert new_data["age"] == 4

def test_session_id():
    ids = set()
    for i in range(0,10000):
        id = session_id()
        assert id not in ids, "id should not have been seen already"
        ids.add(id)

if __name__ == "__main__":
    for i in range(0,10):
        print(session_id())
