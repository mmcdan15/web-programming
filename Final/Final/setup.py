import dataset

if __name__ == "__main__":
    maya_list_db = dataset.connect('sqlite:///maya_list.db') # Creating database, or open if exist
    maya_table = maya_list_db.get_table('things') # check if table exist
    maya_table.drop() # delete table if exist to start fresh
    maya_table = maya_list_db.create_table('things') # creating table
    # filling new table with data
    maya_table.insert_many([
        { 'user' : 'Maya', 'thing' : 'Coding book', 'price' : '40', 'purchased' : 0 },
        { 'user' : 'Maya', 'thing' : 'Pencil', 'price' : '2', 'purchased' : 1 },
        { 'user' : 'Maya', 'thing' : 'Laptop', 'price' : '1200', 'purchased' : 0 },
        { 'user' : 'Ron', 'thing' : 'Whiteboard', 'price' : '30', 'purchased' : 0 },
        { 'user' : 'Ron', 'thing' : 'CEO for dummies crashcourse',  'price' : '29.5', 'purchased' : 1 },
        { 'user' : 'Ron', 'thing' : 'iPad', 'price' : '800', 'purchased' : 0 },

    ])
