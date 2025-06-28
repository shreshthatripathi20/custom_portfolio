from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import json

app = Flask(__name__)

def load_projects():
    with open('projects.json') as f:
        return json.load(f)

#def save_projects(projects):
 #   with open('projects.json', 'w') as f:
  #      json.dump(projects, f, indent=4)

@app.route('/')
def index():
    projects = load_projects()
    return render_template('index.html', projects =projects)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        #Simple login (you can use database instead)
        if username == 'admin' and password == 'admin123':
            session['admin'] = True
            return redirect(url_for('admin'))
        else:
            error = 'Invalid credentials'
        return render_template('login.html', error=error)
    return render_template('login.html', error=error)
@app.route('/admin')
def admin():
    if not session.get('admin'):
        return redirect(url_for('login'))
    return render_template('admin.html')


@app.route('/add', methods=['POST'])
def add_project():
    projects = load_projects()
    new_project = {
        "title": request.form['title'],
        "description": request.form['description'],
        "tech": request.form.getlist('tech')
    }
    projects.append(new_project)
    #save_projects(projects)
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)


# Add update/delete routes here later
