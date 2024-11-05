
from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

app = Flask(__name__) 
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234@localhost/library_management?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app) 


class Books(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey(
        'category.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    publish_year = db.Column(db.Integer, nullable=False)
    author = db.Column(db.String(100), nullable=False)
    publisher = db.Column(db.String(100), nullable=False)
    summary = db.Column(db.Text)
    cover = db.Column(db.String(255), default=None)
    view_count = db.Column(db.Integer, default=0)
    download_count = db.Column(db.Integer, default=0)
    file_path = db.Column(db.String(255), default=None)
    average_rating = db.Column(db.Float, default=0)
    category = db.relationship('Category', back_populates='books')

    def __init__(self, category_id, title, publish_year, author, publisher, summary=None, cover=None, view_count=0, download_count=0,  file_path=None, average_rating=0):
        self.category_id = category_id
        self.title = title
        self.publish_year = publish_year
        self.author = author
        self.publisher = publisher
        self.summary = summary
        self.cover = cover
        self.view_count = view_count
        self.download_count = download_count
        self.file_path = file_path
        self.average_rating = average_rating


class Category(db.Model):
    __table_name__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False)
    image = db.Column(db.String(255))
    books = db.relationship('Books', back_populates='category', lazy=True)

    def __init__(self, category, image=None):
        self.category = category
        self.image = image

@app.route('/')
def home():
    books = Books.query.all()
    categories = Category.query.all()
    totalOfCategories = Category.query.count()
    return render_template('index.html', books=books, categories=categories, totalOfCategories=totalOfCategories)

@app.route('/book/<id>')
def getBookById(id):
    book = Books.query.filter_by(id=id).first()
    category = book.category.category
    return render_template('book_detail.html', book=book, category=category)

@app.route('/books')
def books():
    books = Books.query.all()
    return render_template('book.html', books=books)

@app.route('/categories')
def category():
    categories = Category.query.all()
    return render_template('category.html', categories=categories)

@app.route('/category/<id>')
def getBooksByCategoryId(id):
    category = Category.query.filter_by(id=id).first()
    books = category.books
    return render_template('book.html', books=books)

if __name__ == '__main__':

    app.run(debug=True)
