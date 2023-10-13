import os
from werkzeug.utils import secure_filename
import csv
import random
from flask import Flask, flash, render_template, request, session, redirect, url_for, get_flashed_messages

app = Flask(__name__)
app.secret_key = 'super_secret_key'
app.config['UPLOAD_FOLDER'] = 'uploads'
ALLOWED_EXTENSIONS = {'csv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def load_flashcards(filename):
    cards = []
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            cards.append({
                'id': len(cards),
                'question': row['question'],
                'answer': row['answer'],
                'choices': row['choices'].split(';')
            })
    random.shuffle(cards)  # Randomly shuffle the flashcards.
    return cards

@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/create')
def create():
    return render_template('create.html')

@app.route('/select')
def select():
    messages = get_flashed_messages()
    if messages:
        session.pop('question_base', None)
    session['current_index'] = 0
    session['correct_answers'] = 0
    return render_template('select.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'csvfile' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['csvfile']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        flashcards = load_flashcards(filepath)
        session['question_base'] = flashcards
        os.remove(filepath)
        return redirect(url_for('select'))
    else:
        flash('Invalid file type. Only CSV files are allowed.')
        return redirect(url_for('select'))

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    # Initialize the current_index and correct_answers in the session if not already present
    if 'current_index' not in session:
        session['current_index'] = 0
    if 'correct_answers' not in session:
        session['correct_answers'] = 0

    if session['current_index'] >= len(session['question_base']):
        total_questions = len(session['question_base'])
        correct_answers = session['correct_answers']
        
        # Reset for future quizzes
        session.pop('current_index', None)
        session.pop('correct_answers', None)

        return render_template('result.html', correct=correct_answers, total=total_questions)

    current_flashcard = session['question_base'][session['current_index']]
    if request.method == 'POST':
        if request.form.get('choice') == current_flashcard['answer']:
            session['correct_answers'] += 1
        session['current_index'] += 1
        return redirect(url_for('quiz'))

    return render_template('quiz.html', 
                           flashcard=current_flashcard, 
                           progress=session['current_index'], 
                           total=len(session['question_base']),
                           correct=session['correct_answers'])
if __name__ == '__main__':
    app.run(debug=True)