# minimal example from:
# http://flask.pocoo.org/docs/quickstart/

import os
from flask import Flask, url_for, render_template, request, redirect, session

# from flask.ext.wtf import Form
# from wtforms import StringField, PasswordField, BooleanField, SubmitField
# from wtforms.validators import Required, Length, Email, Regexp, EqualTo
# from wtforms import ValidationError
import numpy as np
import pandas as pd 

#---------- MODEL IN MEMORY ----------------#

# Read the scientific data on breast cancer survival,
# Build a LogisticRegression predictor on it
questions = pd.read_json('beta_QA6.json')
questions.columns=['QA', 'avg', 'difficulty', 'modD','problem']
correct_answers = []
user_answers = []
u_rating = [3]
#---------- URLS AND WEB PAGES -------------#

app = Flask(__name__)

#Form Definition
# class PracticeForm(Form):
#     answer = StringField('Answer', validators=[Required(), Length(1,64)])
#     submit = SubmitField('Submit')


#Views Functions
@app.route('/', methods=['GET','POST'])
def hello_world():
	# form = PracticeForm()
	# user_rating = u_rating[-1]
	# # user_answer=int(request.form['answer'])
	# user_answers.append(user_answer)
	i = np.random.choice(range(50))
	q_row = questions[questions.modD==3]
	qa_list = list(q_row.QA)[0]
	q = qa_list[i][0]
	a = qa_list[i][1]
	correct_answers.append(a)
	# user_qs = questions[(questions.difficulty<user_rating+0.5) & (questions.difficulty>user_rating-0.5) ]
	# q_idx = np.random.choice(range(len(user_qs)))
	# q = questions.ix[q_idx].problem
	# difficulty = questions.ix[q_idx].difficulty
	# last_answer = correct_answers[-2]
	# if user_answer==last_answer:
	# 	user_rating+=0.5
	# else:
	# 	user_rating+=-0.5
	# u_rating.append(user_rating)
	# q_type = np.random.choice(questions.problem)
	return render_template('hello.html', q=q, number=a, correct_answers=correct_answers)
	# return render_template('hello.html', number=x, q=q,
	#  last_answer=last_answer, user_answer=user_answer,
	#   correct_answers=correct_answers, difficulty=difficulty,
	#   user_rating=user_rating, user_answers=user_answers)

@app.route('/practice', methods=['GET','POST'])
def practice():
	user_answer = request.form['answer']
	user_answers.append(user_answer)
	last_answer = correct_answers[-1]

	user_rating = u_rating[-1] #This is the previous user rating prior to their answer.
	if user_rating<6 and user_answer==last_answer:
		user_rating+=1
	elif user_answer!=last_answer and user_rating>1:
		user_rating+=-1
	
	#Now the user's rating has been updated according to their answer.
	#Store this for future reference.
	u_rating.append(user_rating)

	
	

	i = np.random.choice(range(50))
	q_row = questions[questions.modD==user_rating]
	qa_list = list(q_row.QA)[0]
	q = qa_list[i][0]
	a = qa_list[i][1]
	correct_answers.append(a)




	last_answer = correct_answers[-2]


	# u_rating.append(user_rating)
	# q = np.random.choice(questions.problem)
	return render_template('practice.html', q=q, correct_answers=correct_answers,
		number=a, user_answer=user_answer, user_answers=user_answers, last_answer=last_answer,
		user_rating=user_rating, u_rating=u_rating)
	# return render_template('hello.html', number=x, q=q,
	#  last_answer=last_answer, user_answer=user_answer,
	#   correct_answers=correct_answers, difficulty=difficulty,
	#   user_rating=user_rating, user_answers=user_answers)

if __name__ == '__main__':
    app.run()
