from flask import Flask, render_template, request, redirect,flash
from surveys import Survey,Question,satisfaction_survey
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY'] = 'oh-so-secret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
DEBUG = DebugToolbarExtension(app)

RESPONSES = []
# why can I not access the current_page variable in handle_answer?
current_page = 0

@app.route('/')
def get_home_page():
    
    survey_title = satisfaction_survey.title
    survey_instructions = satisfaction_survey.instructions

    return render_template('home.html', survey_title = survey_title, 
    survey_instructions=survey_instructions )

@app.route('/question/<number>')
def get_question(number):
    print(f'current responses are: {RESPONSES}', f'current len is:{len(RESPONSES)}')
    if int(number) != len(RESPONSES):
        flash("Don't skip ahead please!")
        number = len(RESPONSES)
        survey_question =  satisfaction_survey.questions[number].question
        survey_answers = satisfaction_survey.questions[number].choices
        return render_template('question.html',number = number,
        survey_question = survey_question, survey_answers = survey_answers)
    else:
        survey_question =  satisfaction_survey.questions[int(number)].question
        survey_answers = satisfaction_survey.questions[int(number)].choices
  
        return render_template('question.html',number = number,
        survey_question = survey_question, survey_answers = survey_answers)

@app.route('/answer', methods = ['POST'])
def handle_answer():
    question_num = len(RESPONSES)
    max_len = len(satisfaction_survey.questions)
    
    if question_num < max_len -1 :
        answer = request.form
        RESPONSES.append(answer[f'question-{question_num}'])
        # raise
        question_num = len(RESPONSES)
        return redirect(f'/question/{question_num}')
    
    else:
        answer = request.form
        RESPONSES.append(answer[f'question-{question_num}'])
        # raise
        question_num = len(RESPONSES)
        return redirect('/endpage')

@app.route('/endpage')
def end_page():
    print('the responses at endpage are:',RESPONSES)
    return render_template('endpage.html')