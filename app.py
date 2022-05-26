from ast import Delete
import sys
from flask import Flask
from markupsafe import escape
from flask import url_for
from flask import render_template
from flask import request, redirect
import os, json


#from flask_sqlalchemy import SQLAlchemy
#from aplicacion import config
#app.config.from_object(config)

app = Flask(__name__)   



libros = {}
nuevo_id=0
archivo = os.path.join(app.static_folder, 'datos', 'libros.json')
def guardar_libros(libros):
    global archivo
    with open (archivo, 'w') as outfile:
        json.dump(libros,outfile)


@app.route('/')
def principal():
    global archivo
    global libros 
    if not os.path.exists(archivo):
        guardar_libros(libros)
    with open(archivo) as json_file:
        libros = json.load(json_file)
    return render_template("libros/libros.html",libros=libros)


@app.route("/libros/libro/", methods=["GET","POST"])
@app.route("/libros/libro/<int:libro_e>/", methods=["GET","POST"])
def form_libro(libro_e=None):
    libro = {}
    global archivo
    if request.method=="POST":
        global nuevo_id
        global libros
        with open(archivo) as json_file:
            libros= json.load(json_file)
            nuevo_id = len(libros)+1 
        if libro_e:
            nuevo_id = libro_e
        else:
            nuevo_id += 1
        libro["id"] = nuevo_id
        libro["titulo"] = request.form['titulo']
        libro["descripcion"] = request.form['descripcion']
        libro["editorial"] = request.form['editorial']
        libro["noPgns"] = request.form['noPgns']
        libro["fecha"] = request.form['fecha']
        libros[libro["id"]] = libro
        guardar_libros(libros)
        return redirect(url_for("principal"))
    else:
        if libro_e:
            with open(archivo) as json_file:
                libros = json.load(json_file)
            for key, value in libros.items():
                if libros[key]['id']==libro_e:
                 libro_e=value   
    return render_template("libros/form_libro.html", libro_e=libro_e)


@app.route("/libro/<int:id_libro>/")
def mostrar_libro(id_libro):
    global archivo 
    libro_elegido=[]
    with open(archivo) as json_file:
        libros = json.load(json_file)
    for key, value in libros.items():
        if libros[key]['id']==id_libro:
            libro_elegido = value
            print(libro_elegido)
    return render_template("libros/ver_libros.html", libro=libro_elegido)   

@app.route("/libro/<int:id_libro>/")
def button_clicked(id_libro):
    global archivo 
    libro_elegido=[]
    with open(archivo) as json_file:
        libros = json.load(json_file)
    for key, value in libros.items():
        if libros[key]['id']==id_libro:
            del id_libro
            # libro_elegido = value
            # print(libro_elegido)
    return redirect('/')
    
# @app.route("/libro/<int:id_libro>/", methods=["DELETE"])
# def borrarLibro(id_libro):
#     global archivo 
#     libro_elegido=[]
#     with open(archivo) as json_file:
#         libros = json.load(json_file)
#     for key, value in libros.items():
#         if libros[key]['id']==id_libro:
#             json.dumps(libros)
#             break;
#             # libro_elegido = filter(lambda x: libros[key]['id'] != libros[key]['id'], libro_elegido)

#     return render_template("/", libro=libro_elegido)   


if __name__ ==  '__main__':
    app.run(debug=True, port=5000)

# @app.route("/")
#@app.route ("/libro/<int:id_libro>/")
#def form_libro(id_libro=None):
 #   return "formulario{}".format(id_libro)
#@app.route("/libro/libros/")
#@app.route("/libro/libros/<int:id_libro>/")
#def form_libro(id_libro = None):
  #  return render_template("libro/form_libro.html",id_libro=id_libro)



