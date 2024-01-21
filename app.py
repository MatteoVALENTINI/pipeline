from flask import Flask, request, render_template, redirect, url_for
import os
import io
import sys
import subprocess
import unittest
 
app = Flask(__name__)
 
# In-memory database
items = []
 
 
@app.route('/staging', methods=['POST'])
def staging():
    payload = request.json
    ref = payload.get('ref', '')
    response = ('', 204)
    if ref == 'refs/heads/staging':
        os.system("git pull origin staging")
        os.system("pip3 install -r requirements.txt")
        os.system("python -m unittest test-app.py")
        response = 'Test run successfuly'
    return response
 
@app.route('/testing', methods=['POST'])
def testing():
    # Redirection de la sortie standard pour capturer les résultats des tests
    captured_output = io.StringIO()
    sys.stdout = captured_output
 
    # Exécution des tests
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(test-app)  # Assurez-vous que test-app est importé
    unittest.TextTestRunner(stream=captured_output, verbosity=2).run(suite)
 
 
    # Restauration de la sortie standard
    sys.stdout = sys.__stdout__
 
    # Retour des résultats des tests
    return "<pre>" + captured_output.getvalue() + "</pre>"
 
 
@app.route('/deploy', methods=['POST'])
def deploy():
    payload = request.json
    ref = payload.get('ref', '')
    response = ('', 204)
    if ref == 'refs/heads/main':
        subprocess.call(['sh', './deploy.sh'])
        response = 'App is running'
    return response
 
 
@app.route('/')
def index():
    return render_template('index.html', items=items)
 
 
@app.route('/add', methods=['POST'])
def add_item():
    item = request.form.get('item')
    if item:
        items.append(item)
    return redirect(url_for('index'))
 
 
@app.route('/delete/<int:index>')
def delete_item(index):
    if index < len(items):
        items.pop(index)
    return redirect(url_for('index'))
 
 
@app.route('/update/<int:index>', methods=['POST'])
def update_item(index):
    if index < len(items):
        items[index] = request.form.get('new_item')
    return redirect(url_for('index'))
 
 
if __name__ == '__main__':
    app.run(debug=True)  