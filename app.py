from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import csv

app = Flask(__name__)
app.secret_key = 'super_secret_key'

# Load flashcards from CSV file
def load_flashcards(filename='flashcards.csv'):
    cards = []
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            cards.append({
                'question': row['question'],
                'answer': row['answer'],
                'choices': row['choices'].split(';')
            })
    return cards

flashcards = load_flashcards()

@app.route('/')
def index():
    card = flashcards[0]  # For simplicity, just using the first card
    return render_template('index.html', question=card['question'], choices=card['choices'])

@app.route('/check_answer', methods=['POST'])
def check_answer():
    selected_answer = request.form.get('choice')
    correct_answer = flashcards[0]['answer']
    is_correct = selected_answer == correct_answer
    return jsonify({
        'is_correct': is_correct,
        'correct_answer': correct_answer
    })

if __name__ == '__main__':
    app.run(debug=True)