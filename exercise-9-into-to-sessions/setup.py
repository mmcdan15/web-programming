import dataset

if __name__ == "__main__":
    todo_list_db = dataset.connect('sqlite:///todo_list.db')
    todo_table = todo_list_db.get_table('todo')
    todo_table.drop()
    todo_table = todo_list_db.create_table('todo')
    todo_table.insert_many([
        { 'user' : 'greg', 'task' : 'read a book', 'done' : 0 },
        { 'user' : 'greg', 'task' : 'take out the trash', 'done' : 1 },
        { 'user' : 'greg', 'task' : 'do the WP homework', 'done' : 0 },
        { 'user' : 'dorothy', 'task' : 'do not read a book', 'done' : 0 },
        { 'user' : 'dorothy', 'task' : 'do not take out the trash', 'done' : 1 },
        { 'user' : 'dorothy', 'task' : 'do not do the WP homework', 'done' : 0 },

    ])