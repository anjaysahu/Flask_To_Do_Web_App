from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)

# Secret key for session encryption (keeps user data secure)
app.secret_key = 'Secret key has been removed for GitHub'

# Route and function for home page
@app.route('/')
def home():

    # Get user's personal task list from their session
    # If they don't have one yet, create an empty list
    if 'task_list' not in session:
        session['task_list'] = []

    return render_template('index.html', tasks=session['task_list'])

# Route and function for task operations
@app.route('/task', methods=['POST'])
def task_ops():

    # Get operation type from form
    ops = request.form.get("operation")

    # Get user's personal task list from session
    if 'task_list' not in session:
        session['task_list'] = []

    # Handling different operations
    if ops == "add":
        new_task = request.form.get("new_task")

        # Validate and add task to USER'S list
        if new_task.strip():
            session['task_list'].append(new_task)
            session.modified = True  # Tell Flask session changed

    elif ops == "update":
        old_task = request.form.get("old_task")
        new_task = request.form.get("updated_task")

        if old_task in session['task_list'] and new_task.strip():
            task_index = session['task_list'].index(old_task)
            session['task_list'][task_index] = new_task
            # Save back to session
            session.modified = True

    elif ops == "delete":
        task_to_delete = request.form.get("task_to_delete")

        if task_to_delete in session['task_list']:
            session['task_list'].remove(task_to_delete)
            # Save back to session
            session.modified = True

    elif ops == "clear":
        # Clear only USER'S tasks
        session['task_list'] = []
        session.modified = True

    # Redirect back to home page
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)