from flask import Flask, render_template, url_for, request
import os, socket, sys, random, time, math, functools

#####################################################################
#Métodos de ayuda y cálculo
def sample(p):
    x, y = random.random(),random.random()
    return 1 if x*x + y*y < 1 else 0

def calcula_pi(p):
    return 4.0*(functools.reduce(lambda a, b: a + b, map(sample,range(0, p))))/p

#####################################################################

app = Flask(__name__)

@app.route('/')
def hello():
  return render_template('hello.html')

@app.route('/datos')
def datos():
    return render_template('datos.html')

@app.route('/imprime')
def imprime():
    value=os.environ['FLASK_GLOBAL']
    return value

@app.route('/calcula', methods=['GET', 'POST'])
def calcula():
    if request.method=='POST':
        num_puntos=int(request.form['primercampo'])
        start_time = time.time()
        valor=calcula_pi(num_puntos)
        tiempo = time.time()-start_time
        error=abs(math.pi-valor)

        return render_template('calculado.html', puntos=num_puntos, valor=valor, tiempo=tiempo, error=error)
    else :
        return render_template('calcula.html')


@app.route('/conecta', methods=['GET', 'POST'])
def conecta(methods=['POST']):
    if request.method=='POST':
        account_name=int(request.form['account'])
        db_name=int(request.form['db_name'])
        coll_name=int(request.form['coll_name'])
        master_key=int(request.form['master_key'])
        lon=int(request.form['lon'])
        lat=int(request.form['lat'])

if __name__ == '__main__':
  app.run()


