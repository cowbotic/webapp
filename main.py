from flask import Flask, render_template, url_for, request
app = Flask(__name__)

@app.route('/')
def hello():
  return render_template('hello.html')

@app.route('/datos')
def datos():
    return render_template('datos.html')

@app.route('/conecta')
def conecta(methods=['GET', 'POST']):
    if request.method=='POST':
        account_name=int(request.form['account'])
        db_name=int(request.form['db_name'])
        coll_name=int(request.form['coll_name'])
        master_key=int(request.form['master_key'])
        lon=int(request.form['lon'])
        lat=int(request.form['lat'])

if __name__ == '__main__':
  app.run()