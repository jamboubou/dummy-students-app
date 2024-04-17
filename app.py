from flask import Flask, request, render_template, redirect, url_for 
from pymongo import MongoClient 

app = Flask(__name__) 

# MongoDB connection setup 
client = MongoClient(host='ec2-34-229-42-161.compute-1.amazonaws.com', port=27017, 
					username='admin', password='abc123', authSource="admin") 
db = client.studentsdb 
students_collection = db.students 


@app.route('/') 
def home(): 
	students = students_collection.find() 
	return render_template('index.html', students=students) 


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


if __name__ == '__main__': 
	app.run(host='0.0.0.0', debug=True) 
