from flask import Flask, render_template, request, redirect,flash, session
from surveys import Survey,Question,satisfaction_survey
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY'] = 'oh-so-secret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
DEBUG = DebugToolbarExtension(app)


@app.route('/')
def get_home_page():
    """ get the title and instructions from the satisfaction_survey object, which is a Survey 
    instance made of many Question instances"""
    survey_title = satisfaction_survey.title
    survey_instructions = satisfaction_survey.instructions
    # session['RESPONSES'] is set to None, so that a user cannot skip to a question before
    # starting the survey
    session['RESPONSES'] = None
    return render_template('home.html', survey_title = survey_title, 
    survey_instructions=survey_instructions )

@app.route('/new-survey', methods=['POST'])
def start_new_survey():
    # set the session['RESPONSES'] to a new empty array that will collect the user data
    # as well as be used to ensure the user does not skip ahead
    session['RESPONSES'] = []
    return redirect('/question/0') 

@app.route('/question/<int:question_id>')
def get_question(question_id):
    survey_questions_length = len(satisfaction_survey.questions) 
    # if there is no session['RESPONSES'], that means user is at home page trying to skip
    # ahead without starting a new survey. Redirect him to home page and flash message
    if session['RESPONSES'] is None:
        flash("Don't be sneaky, press the start button!")
        return redirect('/')
    """ if the question_id is not the same len as session['RESPONSES'], this means that 
     the user is either trying to skip ahead or go to a previous question -> set the question_id
     to be the len of session['RESPONSES'] which will and bring the user back to the correct
     question"""
    if question_id != len(session['RESPONSES']):
        flash("Don't skip ahead please!")
        question_id = len(session['RESPONSES'])
        survey_question =  satisfaction_survey.questions[question_id].question
        survey_answers = satisfaction_survey.questions[question_id].choices
        return render_template('question.html',question_id = question_id,
        survey_question = survey_question, survey_answers = survey_answers,
        survey_questions_length=survey_questions_length)
        """ the user is not skipping ahead so bring the next question. 
        satisfaction_survey.questions is an array of Question instance"""
    else:
        survey_question =  satisfaction_survey.questions[question_id].question
        survey_answers = satisfaction_survey.questions[question_id].choices
  
        return render_template('question.html',question_id = question_id,
        survey_question = survey_question, survey_answers = survey_answers,
        survey_questions_length=survey_questions_length)

@app.route('/answer', methods = ['POST'])
def handle_answer():
    question_num = len(session['RESPONSES'])
    max_len = len(satisfaction_survey.questions)
    # keeps the logic going as long as there are questions left in the survey
    if question_num < max_len -1 :
        answer = request.form
        print('********************')
        print('current /answer answer is:', answer)
        print('********************')
        res = session['RESPONSES']
        res.append(answer)
        session['RESPONSES'] = res
        
        question_num = len(session['RESPONSES'])
        return redirect(f'/question/{question_num}')
    # when there are no questions left, add the last bit of information and redirect the user to
    # the endpage
    else:
        answer = request.form
        res = session['RESPONSES']
        res.append(answer)
        session['RESPONSES'] = res
        question_num = len(session['RESPONSES'])
        return redirect('/endpage')

@app.route('/endpage')
def end_page():
    print('the responses at endpage are:',session['RESPONSES'])
    
    return render_template('endpage.html')