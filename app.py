'''
This application is a Natural Language based app that utilizes spacy to generate unique words from
either from texts or from documents.
'''



#importing necessary modules

from flask import Flask, render_template, url_for,request
from flask_bootstrap import Bootstrap
from collections import Counter
from docx2python import docx2python
from tika import parser
import spacy
import en_core_web_sm as en
import fr_core_news_sm as fr



#load the languages
nlp_fr = fr.load()
nlp_en = en.load()
pos_tag = ['NOUN', 'PROPN', 'VERB', 'ADJ']

'''
Define a function that checks the type of file uploaded by the client and read it accordingly
Define another function that does the counting of the words
'''

def DocType(source):
	result = source.filename
	#split filename with (.) to get the file extension
	result_splitted = result.split('.')
	file_extension = result_splitted[-1]
	#check the extension type and use appropriate method to read
	if file_extension == "docx":
		doc = docx2python(source).text
		return doc
	elif file_extension == "txt":
		with open(source) as file:
			doc = file.read()
		return doc
	elif file_extension == "pdf":
		raw = parser.from_file(source)
		doc = raw['content']
		return doc

def WordFrequency(document, lang):
	#lang is the language we are loading
	doc_nlp = lang(document)
	word = [token.text for token in doc_nlp
			if not token.is_punct and not token.is_space and not token.is_stop
			and token.pos_ in pos_tag]

	# count the unique words
	word_freq = Counter(word)
	common_word = word_freq.most_common(5)

	# convert to dictionary
	keyword = dict(common_word)
	return keyword

app = Flask(__name__)
#instantiate bootsrap
Bootstrap(app)

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/english')
def english():
    return render_template('english.html')

@app.route('/french')
def french():
    return render_template('french.html')


@app.route('/englishgen', methods = ['POST'] )
def englishgen():
	if request.method == 'POST':
		document = request.files['source-file']
		rawtext = request.form['rawtext']
		file = document.filename
        #if the user does not enter a text

		if file == "" and rawtext == "":
			return render_template('english.html', message = 'Please enter text or upload a file')
		elif rawtext == "":
			#get the file type and count word frequency
			doc_file = DocType(document).lower()
			keyword = WordFrequency(doc_file, nlp_en)
			return render_template('english.html',keyword=keyword, original_text = doc_file)

		elif file == "":
			doc = rawtext.lower()
			#call the WordFrequency function to count the text input
			keyword = WordFrequency(doc, nlp_en)
			return render_template('english.html', keyword=keyword, original_text = doc )


@app.route('/frenchgen', methods = ['POST'] )
def frenchgen():
	if request.method == 'POST':
		document = request.files['source-file']
		rawtext = request.form['rawtext']
		file = document.filename
		# if the user does not enter a text

		if file == "" and rawtext == "":
			return render_template('french.html', message='Please enter text or upload a file')
		elif rawtext == "":
			# get the file type and count word frequency
			doc_file = DocType(document).lower()
			keyword = WordFrequency(doc_file, nlp_fr)
			return render_template('french.html', keyword=keyword, original_text = doc_file)

		elif file == "":
			doc = rawtext.lower()
			# call the WordFrequency function to count the text input
			keyword = WordFrequency(doc, nlp_fr)
			return render_template('french.html', keyword=keyword, original_text = doc)


if __name__ == '__main__':
    app.run(debug=True)