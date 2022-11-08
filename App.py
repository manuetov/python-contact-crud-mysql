from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

# instancio app
app = Flask(__name__)

# inicializa mysql
mysql = MySQL(app)

# Mysql conection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'flaskcontacts'

#settings
app.secret_key = 'mysessionkey'

# ruta raiz 
@app.route('/')
def Index():
   cur = mysql.connection.cursor()
   cur.execute('SELECT * FROM contacts')
   data = cur.fetchall()
   print(data)
   return render_template('index.html', contacts = data)

@app.route('/add_contact', methods=['POST'])
def add_contact():
   if request.method == 'POST':
      name = request.form['nombre']
      surname = request.form['apellidos']
      phone = request.form['telefono']
      email = request.form['email']
      
      # crea la conexión con la bbdd
      cur = mysql.connection.cursor()

      # escribo la consulta con los datos a insertar en la bdd
      cur.execute('INSERT INTO contacts (nombre, apellidos, telefono, email) VALUES (%s, %s, %s, %s)',
       (name, surname, phone, email))

      # ejecuto la consulta. Datos insertados.
      mysql.connection.commit()

      # print(name + ' ' + surname + ' ' + phone + ' ' + email)
      # return 'received'

      # metodo para mostrar texto en html mediante un motor de plantilla
      flash('contacto guardado')
      cur.close()

      return redirect(url_for('Index'))
  
#sin tipar
@app.route('/edit/<id>')
def get_contact(id):
   cur = mysql.connection.cursor()
   cur.execute('SELECT * FROM contacts WHERE id = %s', (id))
   # un solo valor (id)
   data = cur.fetchall() 
   cur.close()
   print(data[0])
   return render_template('edit-contact.html', contact = data[0])

@app.route('/update/<id>', methods=['POST'])
def update_contact(id):
   if request.method == 'POST':
      name = request.form['nombre']
      surname = request.form['apellidos']
      phone = request.form['telefono']
      email = request.form['email']

      cur = mysql.connection.cursor()

      cur.execute(""" 
         UPDATE contacts 
         SET nombre = %s, apellidos = %s, telefono = %s, email = %s
         WHERE id = %s
      """, (name, surname, phone, email, id))

      flash('Contacto actualizado')

      mysql.connection.commit()

      return redirect(url_for('Index'))

#tipado
@app.route('/delete/<string:id>')
def delete_contact(id):
   cur = mysql.connection.cursor()
   cur.execute('DELETE FROM contacts WHERE id ={0}'.format(id))
   mysql.connection.commit()
   flash('Contacto borrado')
   return redirect(url_for('Index'))

# si el nombre es igual al modulo principal main 
if __name__ == '__main__':
   # debug => reinicia el server con cada cambio - tipo nodemon o lifeserver 
   app.run(port = 3000, debug = True)