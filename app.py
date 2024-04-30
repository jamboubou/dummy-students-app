from flask import Flask, request, render_template, redirect, url_for 
from pymongo import MongoClient 
from kubernetes import client, config
import requests

app = Flask(__name__) 

# Get MongoDB connection parameters from file
with open('config', 'r') as f:
	db_config = f.read().splitlines()
	host = db_config[0]
	port = db_config[1]
	username = db_config[2]
	password = db_config[3]
	authSource = db_config[4]
	f.close()
	

# MongoDB connection setup 
client = MongoClient(host=host, port=port, 
					username=username, password=password, authSource=authSource) 
db = client.studentsdb 
students_collection = db.students 

# Home route to display all students
@app.route('/') 
def home(): 
	students = students_collection.find() 
	return render_template('index.html', students=students) 

# add_student route to add a new student
@app.route('/add_student', methods=['POST']) 
def add_student(): 
	if request.method == 'POST': 
		student_data = { 
			'name': request.form['name'], 
			'roll_number': request.form['roll_number'], 
			'grade': request.form['grade'] 
		} 
		students_collection.insert_one(student_data) 
	return redirect(url_for('home')) 

# search_student route to search for a student by name, roll number or grade
@app.route('/search_student', methods=['POST'])
def search_student():
	if request.method == 'POST':
		search_term = request.form['search_term']
		students = students_collection.find({
			'$or': [
				{'name': {'$regex': search_term, '$options': 'i'}},
				{'roll_number': {'$regex': search_term, '$options': 'i'}},
				{'grade': {'$regex': search_term, '$options': 'i'}}
			]
		})
		return render_template('index.html', students=students)

# Fetch url
@app.route('/fetch', methods=['GET', 'POST'])
def fetch_url():
    if request.method == 'GET':
        url = request.args.get('url')
    elif request.method == 'POST':
        url = request.form.get('url')

    if not url:
        return 'Please provide a URL'

    try:
        response = requests.get(url)
        return response.text
    except:
        return 'Unable to fetch URL'
	
if __name__ == '__main__': 
	app.run(host='0.0.0.0', debug=True) 
