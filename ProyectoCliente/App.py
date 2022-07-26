from types import NoneType
from django.db import connection
from flask import Flask, render_template, request, redirect, url_for, flash, Response
from flask_mysqldb import MySQL
import pymysql
import io
import csv

app = Flask(__name__)

# Mysql Conexion.
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='teor'
app.config['MYSQL_PASSWORD']='teor'
app.config['MYSQL_DB']='procliente'
mysql=MySQL(app)

#Sentencia.
app.secret_key= 'mysecretkey'

@app.route('/')
def Index():
    cur=mysql.connection.cursor()
    cur.execute('SELECT * FROM info_cliente')
    data=cur.fetchall()
    return render_template('index.html', infocontacto=data)

########################################################################################

# INGRESAR INFORMACION DEL CLIENTE

@app.route('/add_contacto', methods=['POST'])
def add_contacto():
    if request.method=='POST':
        Nombre=request.form['Nombre']
        Apellido=request.form['Apellido']
        FechaNacimiento=request.form['Fechanacimiento']
        Genero=request.form['Genero_c']
        Telefono=request.form['Telefono']
        Correo=request.form['Correo']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO info_cliente (Nombre, Apellido, Fechanacimiento, Genero_c, Telefono, Correo) VALUES (%s, %s, %s, %s, %s, %s)', 
        (Nombre, Apellido, FechaNacimiento, Genero, Telefono, Correo))
        mysql.connection.commit()
        flash('Contacto agregado satisfactoriamente')
        return redirect(url_for('Index'))

# EDITAR DIRECCIONES
        
@app.route('/edi_contacto/<id>')
def edi_contacto(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM info_cliente WHERE id_cliente = %s', (id,))
    return render_template('editarcontacto.html', contacto=cur.fetchone())

@app.route('/editar/<id>', methods = ['POST'])
def editar_contacto(id):
    if request.method=='POST':
        Nombre=request.form['Nombre']
        Apellido=request.form['Apellido']
        FechaNacimiento=request.form['Fechanacimiento']
        Genero=request.form['Genero_c']
        Telefono=request.form['Telefono']
        Correo=request.form['Correo']
    cur = mysql.connection.cursor()
    cur.execute(""" 
    UPDATE info_cliente
    SET Nombre=%s,
    Apellido=%s,
    Fechanacimiento=%s,
    Genero_c=%s,
    Telefono=%s,
    Correo=%s
    WHERE id_cliente=%s
    """,(Nombre, Apellido, FechaNacimiento, Genero, Telefono, Correo, id))
    mysql.connection.commit()
    flash('Contacto editado satisfactoriamente')
    return redirect(url_for('Index'))

# ELIMNAR CLIENTE 

@app.route('/eli_contacto/<id>')
def eli_contacto(id):
    cur=mysql.connection.cursor()
    cur.execute('DELETE FROM info_cliente WHERE id_cliente = {0}'.format(id))
    mysql.connection.commit()
    flash("Contacto eliminado satisfactoriamente")
    return redirect(url_for('Index'))

#################################################################################################

# INGRESAR DIRECCIONES

@app.route('/direcciones/<id>', methods=['GET', 'POST'])
def direcciones(id):
    if request.method=='GET':
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM ct_direccion WHERE cliente_id= %s', (id,))
        return render_template('direccion.html', infodireccion = cur.fetchall(), direccion=id)
    
    if request.method=='POST':
        Pais=request.form['Pais']
        Departamento=request.form['Departamento']
        Municipio=request.form['Municipio']
        Direccion=request.form['Direccion']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO ct_direccion  VALUES (NULL, %s, %s, %s, %s, %s)', 
        (Pais, Departamento, Municipio, Direccion, id))
        mysql.connection.commit()
        flash('Contacto agregado satisfactoriamente')
        return redirect(url_for('direcciones', id=id))

#EDITAR DIRECCION
def get_direccion_from_id(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM ct_direccion WHERE id_direccion= %s', (id,))
    return cur.fetchone()

@app.route('/edi_direccion/<id_direccion>', methods=['GET', 'POST'])
def edi_direcciones(id_direccion):
    if request.method=='GET':
        return render_template('editardireccion.html', Direccion=get_direccion_from_id(id_direccion))
    
    if request.method=='POST':
        Pais=request.form['Pais']
        Departamento=request.form['Departamento']
        Municipio=request.form['Municipio']
        Direccion=request.form['Direccion']
        cur = mysql.connection.cursor()
        cur.execute(""" 
        UPDATE ct_direccion
        SET Pais=%s,
        Departamento=%s,
        Municipio=%s,
        Direccion=%s
        WHERE id_direccion=%s
        """,(Pais, Departamento, Municipio, Direccion,id_direccion))
        mysql.connection.commit()
        Direccion=get_direccion_from_id(id_direccion)
        flash('Contacto editado satisfactoriamente')
        return redirect(url_for('direcciones', id=Direccion[5]))

#ELIMINAR DIRECCIONES
@app.route('/eli_direccion/<id>')
def eli_direccion(id):
    cliente_id=get_direccion_from_id(id)[5]
    cur=mysql.connection.cursor()
    cur.execute('DELETE FROM ct_direccion WHERE id_direccion = {0}'.format(id))
    mysql.connection.commit()
    
    flash("Contacto eliminado satisfactoriamente")
    return redirect(url_for('direcciones', id=cliente_id))

###############################################################################################

#IGRESAR DOCUMENTOS
def get_documento_from_id(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM tpdocumento WHERE id_documento= %s', (id,))
    return cur.fetchone()

@app.route('/documentos/<id>', methods=['GET', 'POST'])
def documentos(id):
    if request.method=='GET':
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM tpdocumento WHERE clientedoc_id= %s', (id,))
        return render_template('documento.html', infodocumento = cur.fetchall(), documento=id)

    if request.method=='POST':
        Tipodoc=request.form['Tipodocumento']
        Numerodoc=request.form['Numerodocumento']
        cur=mysql.connection.cursor()
        cur.execute('INSERT INTO tpdocumento VALUES (NULL, %s, %s, %s)', (Tipodoc, Numerodoc, id))
        mysql.connection.commit()
        flash('Documento agregado con exito')
        return redirect(url_for('documentos', id=id))

# EDITAR DOCUMENTOS
def get_documento_id(id):
    cur=mysql.connection.cursor()
    cur.execute('SELECT * FROM tpdocumento WHERE id_documento=%s', (id,))
    return cur.fetchone()
    
@app.route('/edi_documento/<id_documento>', methods=['GET', 'POST'])
def edi_documento(id_documento):
    if request.method=='GET':
        return render_template('edidocumento.html', Documento=get_documento_id(id_documento))

    if request.method=='POST':
        Tipodoc=request.form['Tipodocumento']
        Numerodoc=request.form['Numerodocumento']
        cur=mysql.connection.cursor()
        cur.execute(""" 
        UPDATE tpdocumento
        SET Tipodocumento=%s,
        Numerodoc=%s
        WHERE id_documento=%s
        """,(Tipodoc, Numerodoc, id_documento))
        mysql.connection.commit()
        Documento = get_documento_id(id_documento)
        flash('Documento editado exitosamente')
        return redirect(url_for('documentos', id=Documento[3]))

#ELIMINAR DOCUMENTO
@app.route('/eli_documento/<id>')
def eli_documento(id):
    clientedoc_id=get_documento_from_id(id)[3]
    cur=mysql.connection.cursor()
    cur.execute('DELETE FROM tpdocumento WHERE id_documento = {0}'.format(id))
    mysql.connection.commit()
    
    flash("Contacto eliminado satisfactoriamente")
    return redirect(url_for('documentos', id=clientedoc_id))   

        
    

if __name__=='__main__':
    app.run(port=3000, debug=True)  