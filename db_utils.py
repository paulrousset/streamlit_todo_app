import sqlite3
conn = sqlite3.connect("data.db", check_same_thread=False)
c = conn.cursor()


def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS tasktable(task TEXT, task_status TEXT, task_due_date DATE)')


def add_data(task, task_status, task_due_date):
    c.execute('INSERT INTO tasktable(task, task_status, task_due_date) VALUES (?,?,?)', (task, task_status,
                                                                                         task_due_date))
    conn.commit()


def view_all_data():
    c.execute('SELECT * FROM tasktable')
    data = c.fetchall()
    return data


def view_unique_tasks():
    c.execute('SELECT DISTINCT task FROM tasktable')
    data = c.fetchall()
    return data


def get_task(task):
    c.execute('SELECT * FROM tasktable WHERE task="{}"'.format(task))
    # c.execute('SELECT * FROM tasktable WHERE task = ?', (task) )
    data = c.fetchall()
    return data


def edit_task_data(new_task, new_task_status, new_task_due_date, task):
    c.execute("UPDATE tasktable SET task = ?, task_status=?, task_due_date=? WHERE task = ? ", (new_task, new_task_status, new_task_due_date, task))
    conn.commit()
    data = c.fetchall()
    return data


def delete_task(task):
    c.execute('DELETE FROM tasktable WHERE task = "{}"'.format(task))
    conn.commit()

