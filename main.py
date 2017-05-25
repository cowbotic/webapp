from flask import Flask, render_template, url_for, request
import os, socket, sys, random, time, math, functools
import pydocumentdb.document_client as document_client

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
        account_name=request.form['account']
        db_name=request.form['db_name']
        coll_name=request.form['coll_name']
        master_key=request.form['master_key']
        lon=float(request.form['lon'])
        lat=float(request.form['lat'])
        maps_api_key=request.form['maps_key']
        distancia_centro=str(request.form['dist'])

        cliente = document_client.DocumentClient('https://'+account_name+'.documents.azure.com', {'masterKey': master_key})
        bbdd=cliente.ReadDatabase('dbs/'+db_name)
        coleccion=cliente.ReadCollection('dbs/'+db_name+'/colls/'+coll_name)
        id_coleccion=coleccion['_self']
               
        opciones={}
        opciones['enableCrossPartitionQuery'] = True
        consulta='SELECT c.Location.coordinates[0] as lon, c.Location.coordinates[1] as lat, c.mass_grams as masa, c.Name as nombre FROM c WHERE ST_DISTANCE(c.Location, { "type": "Point", "coordinates": ['+str(lon)+', '+str(lat)+'] }) <'+distancia_centro

        salida = cliente.QueryDocuments(id_coleccion,consulta,opciones)
        lista_salida=salida.fetch_next_block()

        with open ('static/sitios.js','w') as fichero:
            fichero.write('myData = [\n')
            for elem in lista_salida:
                m_name=elem['nombre'].replace(u"\ufeff", "")[1:].replace("'","`")
                fichero.write('['+str(elem['lat'])+','+str(elem['lon'])+','+"'"+m_name+': '+str(elem['masa'])+" gramos'"+'],\n')
            fichero.write('];')
            fichero.close()
        return render_template('mapa.html', latitud=lat, longitud=lon, maps_api_key=maps_api_key)
        


if __name__ == '__main__':
  app.run()


