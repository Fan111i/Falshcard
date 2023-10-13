from flask import Flask, render_template, request, session, redirect, url_for, flash
import csv
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'super_secret_key'

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
    return cards

@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/create')
def create():
    return render_template('create.html')

@app.route('/create_flashcard', methods=['POST'])
def create_flashcard():
    question = request.form['question']
    answer = request.form['answer']
    choices = request.form.getlist('choices')
    flashcards = session.get('flashcards', [])
    flashcards.append({'id': len(flashcards), 'question': question, 'answer': answer, 'choices': choices})
    session['flashcards'] = flashcards
    return redirect(url_for('select'))

@app.route('/select')
def select():
    flashcards = session.get('flashcards', [])
    return render_template('select.html', flashcards=flashcards)

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
        # Sort the flashcards by question
        flashcards.sort(key=lambda x: x['question'])
        session['question_base'] = flashcards  # Save the uploaded flashcards directly to the base
        session['current_index'] = 0
        session['correct_answers'] = 0
        os.remove(filepath) 
        return redirect(url_for('quiz'))

    flash('Invalid file type')
    return redirect(request.url)

@app.route('/add_to_base', methods=['POST'])
def add_to_base():
    flashcards = session.get('flashcards', [])
    selected_ids = request.form.getlist('selected')
    session['question_base'] = [flashcards[int(i)] for i in selected_ids]
    session['current_index'] = 0
    session['correct_answers'] = 0
    return redirect(url_for('quiz'))

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if 'current_index' not in session or session['current_index'] >= len(session['question_base']):
        return render_template('result.html', correct=session['correct_answers'], total=len(session['question_base']))

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
    # Ensure the UPLOAD_FOLDER exists
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)