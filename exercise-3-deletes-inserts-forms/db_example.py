import dataset

if __name__ == "__main__":
    todo_list_db = dataset.connect('sqlite:///todo_list.db')
    todo_table = todo_list_db.get_table('todo')
    result = todo_list_db.query("select * from todo")
    result = [ dict(x) for x in list(result) ]
    print(result)    
    result = todo_table.find()
    result = [ dict(x) for x in list(result) ]
    print(result)