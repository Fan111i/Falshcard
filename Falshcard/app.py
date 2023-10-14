from flask import Flask, render_template, Response, request, session, redirect, url_for
import csv
import os

app = Flask(__name__)
app.secret_key = 'super_secret_key'

app.config['UPLOAD_FOLDER'] = 'multimedia'

ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif', 'mp3']

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def load_flashcards(filename='flashcards.csv'):
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

def save_flashcard(question, answer, choices, filename='flashcards.csv'):
    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([question, answer, ";".join(choices)])

def load_multimedia(filename='multimedia.csv'):
    multimedia = []
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            multimedia.append({
                'id': len(multimedia),
                'file_type': row['file_type'],
                'file_name': row['file_name'],
                'question': row['question']
            })
    return multimedia

def save_multimedia(file_type, file_name, question, filename='multimedia.csv'):
    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([file_type, file_name, question])

@app.route('/')
def homepage():

    return render_template('homepage.html')

@app.route('/create')
def create():
    return render_template('create.html')

@app.route('/multimedia/<name>')
def get_multimedia(name):
    file_type = name.split('.')[-1]
    with open(os.path.join(app.config['UPLOAD_FOLDER'], name), 'rb') as file:
        image = file.read()
        resp = Response(image, mimetype="image/{}".format(file_type))
        return resp

@app.route('/create_multimedia')
def create_media():
    return render_template('create_multimedia.html')

@app.route('/create_flashcard', methods=['POST'])
def create_flashcard():
    question = request.form['question']
    answer = request.form['answer']
    choices = request.form.getlist('choices')
    save_flashcard(question, answer, choices)
    return redirect(url_for('select'))

@app.route('/create_multimedia', methods=['POST'])
def create_multimedia():
    question = request.form['question']
    file = request.files['file']
    print(question, file)
    if file and allowed_file(file.filename):
        file_name = file.filename
        file_type = file_name.split('.')[-1]
        save_multimedia(file_type, file_name, question)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
    else:
        print('File not allowed')
        return redirect(url_for('create_multimedia'))
    return redirect(url_for('select'))

@app.route('/select')
def select():
    flashcards = load_flashcards()
    multimedia = load_multimedia()
    return render_template('select.html', flashcards=flashcards, multimedia=multimedia)

@app.route('/add_to_base', methods=['POST'])
def add_to_base():
    flashcards = load_flashcards()
    multimedia = load_multimedia()
    selected_ids = request.form.getlist('selected')
    selected_multimedia_ids = request.form.getlist('selected_multimedia')
    session['question_base'] = [flashcards[int(i)] for i in selected_ids]
    session['multimedia_base'] = [multimedia[int(i)] for i in selected_multimedia_ids]
    session['current_index'] = 0
    session['correct_answers'] = 0
    return redirect(url_for('quiz'))

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if 'current_index' not in session or session['current_index'] >= len(session['question_base']):
        return render_template('result.html', correct=session['correct_answers'], total=len(session['question_base']))

    current_flashcard = session['question_base'][session['current_index']]
    multimedias = session['multimedia_base']
    if request.method == 'POST':
        if request.form.get('choice') == current_flashcard['answer']:
            session['correct_answers'] += 1
        session['current_index'] += 1
        return redirect(url_for('quiz'))

    return render_template('quiz.html', 
                           flashcard=current_flashcard, 
                           multimedia=multimedias,
                           progress=session['current_index'], 
                           total=len(session['question_base']),
                           correct=session['correct_answers'])

if __name__ == '__main__':
    app.run(debug=True)