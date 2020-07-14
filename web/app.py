from flask import Flask, request, jsonify, render_template, url_for, redirect
import pandas as pd
import re

app = Flask(__name__)
book_df = pd.read_csv('booksummaries.txt',error_bad_lines=False,delimiter="\t",header=None,\
                      names=["BookID", "Unknown", "Title","Author","Published Date","Tags","Summary"])

cos_df = pd.read_pickle("cos_5000rows.pkl")
@app.route("/")
def home():
	return render_template("index.html", content='hello')

@app.route("/api")
def api():
	books = {620: 'Animal Farm', 241961: 'My Family and Other Animals', 523886: 'Exercitatio Anatomica de Motu Cordis et Sanguinis in Animalibus', 632999: 'Animal World', 2066549: 'Animal Dreams', 3765583: 'The Dying Animal', 8206943: 'The Animals of Farthing Wood', 11431117: 'The Moral Animal', 16629981: 'The Animal Family', 17392692: 'Pack Animals', 21760308: 'Animal Spirits: How Human Psychology Drives the Economy, and Why It Matters for Global Capitalism', 31324723: 'The God of Animals'}

	return jsonify(books)

@app.route("/search", methods=['GET'])
def search():
	term = request.args.get('term') #request.args.get apply for GET method
	books = list()
	for book in book_df['Title']:
	    book_lower = book.lower()
	    if bool(re.search(f".*{term}.*", book_lower)):
	        book_id = int(book_df.query("Title == @book").iloc[0,0])
	        books.append({'id':book_id, 'value':book})
	return jsonify(books)

@app.route("/book_recommendation", methods=['GET'])
def book_recommendation():
	book_title= request.args.get('title')
	number_recommendation = request.args.get('number')
	recommendations = list(cos_df[book_title].sort_values(ascending=False)[1: 1+int(number_recommendation)].index)
	return jsonify(recommendations)

if __name__ == "__main__":
	app.run(debug=True)