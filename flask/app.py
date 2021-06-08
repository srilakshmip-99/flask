from flask import Flask, request, render_template,redirect,url_for,flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key="secret key"

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/book'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Data(db.Model):
    __tablename__ ='Data'
    book_id = db.Column(db.String(25), primary_key=True)
    title = db.Column(db.String(100))
    author = db.Column(db.String(100))
    publisher = db.Column(db.String(100))

    def __init__(self,book_id,title,author,publisher):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.publisher = publisher


@app.route('/')
def Index():
    all_data = Data.query.all()

    return render_template('index.html',book = all_data)

#-------------INSERT-------------------
@app.route('/insert',methods = ['POST'])
def insert():
    if request.method == 'POST':
        book_id = request.form['book_id']
        title = request.form['title']
        author = request.form['author']
        publisher = request.form['publisher']

        my_data = Data(book_id,title,author,publisher)
        db.session.add(my_data)
        db.session.commit()

        flash("Book inserted sucessfully")

        return redirect(url_for('Index'))

#  ---------------UPDATE----------------
@app.route('/update',methods = ['GET','POST'])
def update():
    if request.method == 'POST':
        my_data = Data.query.get(request.form.get('book_id'))

        #my_data.book_id = request.form['book_id']
        my_data.title = request.form['title']
        my_data.author = request.form['author']
        my_data.publisher = request.form['publisher']

        db.session.commit()
        flash("Book updated successfully")

        return redirect(url_for('Index'))

#-----------DELETE---------------
@app.route('/delete/<id>', methods = ['GET','POST'])
def delete(id):
    my_data = Data.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Book Deleted successfully")

    return redirect(url_for('Index'))


if __name__=="__main__":
    app.run(debug=True)