import dataset

if __name__ == "__main__":
    todo_list_db = dataset.connect('sqlite:///todo_list.db')
    todo_table = todo_list_db.get_table('todo')
    todo_table.drop()
    todo_table = todo_list_db.create_table('todo')
    todo_table.insert_many([
        { 'task' : 'read a book', 'done' : 0 },
        { 'task' : 'take out the trash', 'done' : 1 },
        { 'task' : 'do the WP homework', 'done' : 0 },
    ])