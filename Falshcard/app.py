from flask import Flask, render_template, request, session, redirect, url_for, Response
import csv
from random import randrange
import json
import glob
import os
import math
import copy
import pandas as pd
import numpy as np

app = Flask(
    __name__,
    static_url_path='', 
    static_folder='static'
)
app.secret_key = 'super_secret_key'

app.config['UPLOAD_FOLDER'] = os.path.join("Falshcard", "multimedia")

ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif', 'mp3','mp4']

ALLOWED_IMAGES = ['png', 'jpg', 'jpeg', 'gif']

def allowed_images(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGES 

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def program_directory():
    try:
        return os.path.dirname(os.path.abspath(__file__))
    except Exception:
        return os.getcwd()
    

@app.route('/')
def homepage():
    decks = glob.glob(program_directory() + "/*.csv")
    numbered_paths_and_names = deck_menu_constructor(decks)
    # makes a variable to hold the list of deck names with a given number starting at 1
    decks_choice_display = []
    for name_path_tup in numbered_paths_and_names:
        if str(name_path_tup[1]) != 'users':
            decks_choice_display.append({'id': str(name_path_tup[0]), 'name': str(name_path_tup[1])})

    # Deck choice menu prompt
    session['deck_chosen'] = False
    return render_template('homepage.html', decks_choice_display = decks_choice_display)

@app.route('/contact')
def contact():
    decks = glob.glob(program_directory() + "/*.csv")
    numbered_paths_and_names = deck_menu_constructor(decks)
    # makes a variable to hold the list of deck names with a given number starting at 1
    decks_choice_display = []
    for name_path_tup in numbered_paths_and_names:
        if str(name_path_tup[1]) != 'users':
            decks_choice_display.append({'id': str(name_path_tup[0]), 'name': str(name_path_tup[1])})

    # Deck choice menu prompt
    session['deck_chosen'] = False
    return render_template('contact.html', decks_choice_display = decks_choice_display)

@app.route('/signin', methods=['GET'])
def signin():
    decks = glob.glob(program_directory() + "/*.csv")
    numbered_paths_and_names = deck_menu_constructor(decks)
    # makes a variable to hold the list of deck names with a given number starting at 1
    decks_choice_display = []
    for name_path_tup in numbered_paths_and_names:
        if str(name_path_tup[1]) != 'users':
            decks_choice_display.append({'id': str(name_path_tup[0]), 'name': str(name_path_tup[1])})

    # Deck choice menu prompt
    session['deck_chosen'] = False
    return render_template('signin.html', decks_choice_display = decks_choice_display)

@app.route('/signup', methods=['GET'])
def signup():
    decks = glob.glob(program_directory() + "/*.csv")
    numbered_paths_and_names = deck_menu_constructor(decks)
    # makes a variable to hold the list of deck names with a given number starting at 1
    decks_choice_display = []
    for name_path_tup in numbered_paths_and_names:
        if str(name_path_tup[1]) != 'users':
            decks_choice_display.append({'id': str(name_path_tup[0]), 'name': str(name_path_tup[1])})

    # Deck choice menu prompt
    session['deck_chosen'] = False
    return render_template('signup.html', decks_choice_display = decks_choice_display)

def load_users(filename="users.csv"):
    users = []
    with open(program_directory() + '/' + filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            print(row)
            users.append({
                'id': len(users),
                'username': row['username'],
                'email': row['email'],
                'password': row['password']
            })
    return users

def save_user(username, email, password, filename='users.csv'):
    with open(program_directory() + '/' + filename, 'a', newline='') as file:
        writer = csv.writer(file)
        csv.unregister_dialect
        writer.writerow([username, email, password])

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    cpassword = request.form['cpassword']
    print(username, email, password, cpassword)
    if password != cpassword:
        return redirect(url_for('signup'))
    users = load_users('users.csv')
    for user in users:
        if user['username'] == username or user['email'] == email:
            return redirect(url_for('signup'))
    save_user(username, email, password)
    return redirect(url_for('signin'))

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    users = load_users('users.csv')
    for user in users:
        if user['username'] == username and user['password'] == password:
            decks = glob.glob(program_directory() + "/*.csv")
            numbered_paths_and_names = deck_menu_constructor(decks)
            # makes a variable to hold the list of deck names with a given number starting at 1
            decks_choice_display = []
            for name_path_tup in numbered_paths_and_names:
                if str(name_path_tup[1]) != 'users':
                    decks_choice_display.append({'id': str(name_path_tup[0]), 'name': str(name_path_tup[1])})

            # Deck choice menu prompt
            session['deck_chosen'] = False
            session['username'] = username
            return render_template('main.html', decks_choice_display = decks_choice_display)
    return render_template('signin')

@app.route('/create')
def create():
    return render_template('create.html')

def load_flashcards(filename='flashcards.csv'):
    cards = []
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            cards.append({
                'id': len(cards),
                'question': row['question'],
                'answer': row['answer'],
                'file_type': row['file_type'],
                'file_name': row['file_name'],
                'choices': row['choices'].split(';')
            })
    return cards
    
    # cards = []
    # df=pd.read_csv(filename)
    # data = np.array(df)
    # for row in data:
    #     print(row)
    #     cards.append({
    #         'id': len(cards),
    #         'question': row[0],
    #         'answer': row[1],
    #         'choices': row[2].split(';')
    #     })
    # print(cards)
    # return cards

def save_flashcard(question, answer, choices, file_type, file_name, filename='flashcards.csv'):
    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)
        csv.unregister_dialect
        writer.writerow([question, answer, ";".join(choices), file_type, file_name])
        
def del_flashcard(question, filename='flashcards.csv'):
    df=pd.read_csv(filename)
    df = df[~df['question'].eq(question)]
    df.to_csv(filename, index=False)

@app.route('/multimedia/<name>')
def get_multimedia(name):
    file_type = name.split('.')[-1]
    if file_type and allowed_images(name):
        with open(os.path.join(app.config['UPLOAD_FOLDER'], name), 'rb') as file:
            image = file.read()
            resp = Response(image, mimetype="image/{}".format(file_type))
            return resp
    else:
        def generate():
            with open(os.path.join(app.config['UPLOAD_FOLDER'], name), "rb") as fwav:
                data = fwav.read(1024)
                while data:
                    yield data
                    data = fwav.read(1024)
        resp = Response(generate(), mimetype="audio/mpeg")
        return resp

@app.route('/create_flashcard', methods=['POST'])
def create_flashcard():
    question = request.form['question']
    answer = request.form['answer']
    choices = request.form.getlist('choices')
    file = request.files['file']
    if file and allowed_file(file.filename):
        file_name = file.filename
        file_type = file_name.split('.')[-1]
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
        save_flashcard(question, answer, choices, file_type, file_name)
    else:
        save_flashcard(question, answer, choices, '', '')
    return redirect(url_for('select'))

@app.route('/select')
def select():
    flashcards = load_flashcards('flashcards(chinese elements).csv')
    return render_template('select.html', flashcards=flashcards)
    
def import_quizlet_lineskip_fix(filepath, fbsep="\t", cardsep="\n"):
    """
    Take a Quizlet flashcard export either that by default uses tab for card front and back,
and linebreak for new card, or a custom export that uses custom characters to separate.

If a line doesnt have a tab, join with a "\n" to the line before it.

write a new file to same directory, using the same filename but changing the extension to .json

    :param str filepath: File path of file to be converted, must be a .txt file
    :param str fbsep: Separation value between front and back of card, default is tab "\t.
    :param str cardsep: Separation value between card and card, default is linebreak "\n".
    :return dict: converted dictionary.
    """
    with open(filepath, encoding='utf-8') as fileobj:
        data0 = fileobj.readlines()
    # First combine all lines into a long string.
    data1 = ""
    for line1 in data0:
        data1 += line1
    # Then split by the cardsep
    data3 = data1.split(cardsep)
    # For default setting, we must rejoin the lines that were separated by a linebreak
    if cardsep == "\n":
        clean_counter = 0
        while clean_counter < len(data3):
            clean_counter = 0
            for itm0 in data3:
                if fbsep not in itm0:
                    data3[data3.index(itm0)-1] += "\n" + data3.pop(data3.index(itm0))
                    break
                elif fbsep in itm0:
                    clean_counter += 1
    # Then cull entries with too many fbsep's
    for itm1 in data3:
        if itm1.count(fbsep) > 1:
            # Reverse replace method
            data3[data3.index(itm1)] = "\n".join(itm1.rsplit(fbsep, 1))
    # Then separate by fbsep, culling trailing punctuation on the way
    data4 = []
    for itm2 in data3:
        if itm2 != "" and itm2 != "\n" and itm2 != "":
            data4.append(itm2.split(fbsep))
    # Then clean out wrong sized items, making sure our list of paired strings lists are all len(2) pairs
    data5 = []
    for itm3 in data4:
        if len(itm3) != 2:
            print(f"Item: '{itm3}' was not included in the deck.")
        else:
            data5.append(itm3)
    # Finally make the dictionary
    data6 = dict(data5)
    # Write the dictionary to a new file with the same name, but a .json extension
    write_file_path = os.path.splitext(filepath)[0] + ".json"
    write_to_file = open(write_file_path, 'w+')
    write_to_file.write(json.dumps(data6, sort_keys=True, indent=4))
    write_to_file.close()
    return data6


def deck_menu_constructor(paths):
    """
    Takes a list of file paths and returns a three part tuple with a label number,
the truncated filename, and the file path.

    :param list paths: a list of file file paths, must be json files containing dictionaries
    :return: a list of three part tuples (number, filename, file path)
    """
    output_list = []
    counter = 1
    for path in paths:
        file_name_w_ext = os.path.basename(path)
        file_name, file_ext = os.path.splitext(file_name_w_ext)
        tup = (counter, file_name, path)
        counter += 1
        output_list.append(tup)
    return output_list


def get_deck():
    deck_choice = session['deck_choice']
    decks = glob.glob(program_directory() + "/*.csv")
    numbered_paths_and_names = deck_menu_constructor(decks)
    filename = numbered_paths_and_names[int(deck_choice) - 1][2]
    deck = load_flashcards(filename)
    session['filename'] = filename
    
    # deck_choice = session['deck_choice']
    # decks = glob.glob(program_directory() + "/*.json")
    # numbered_paths_and_names = deck_menu_constructor(decks)
    # file_to_open = open(numbered_paths_and_names[int(deck_choice) - 1][2], 'r')
    # deck = json.loads(file_to_open.read())
    # file_to_open.close()
    return deck

def card_displayer(card):
    """Take a string and put a box graphic around it. Returns a multiline string"""
    def grid_builder(cardstr, rowlen=80):
        """Take a string and make it into a list of items not more than rowlen long"""
        initial_grid = cardstr.split("\n")
        grid = []
        for itm in initial_grid:
            if len(itm) <= rowlen:
                grid.append(itm)
            else:
                to_grid = []
                x = 0
                times_through = 1
                while len(to_grid) < len(itm) // rowlen + 1:
                    if len(itm[x:]) > rowlen:
                        if itm[x + rowlen -1].isalpha() and itm[x + rowlen] != " ":
                            to_grid.append(itm[x: x + rowlen].lstrip() + "-")
                            x += rowlen
                        else:
                            to_grid.append(itm[x: x + rowlen].lstrip())
                            x += rowlen
                    else:
                        to_grid.append(itm[x:].lstrip())

                for itm2 in to_grid:
                    grid.append(itm2)
        return grid

    def out_put_builder(grid):
        """Put lines around strings in a grid"""
        output = ""
        longest_line = 0
        for itm3 in grid:
            if len(itm3) > longest_line:
                longest_line = len(itm3)
        top_line = '\n__' + ('_' * longest_line) + '__\n'
        empty_line = '| ' + (' ' * longest_line) + ' |\n'
        bottom_line = '|_' + ('_' * longest_line) + '_|\n'

        def text_line(column):
            white_space = longest_line - len(grid[column])
            text_lne = '| ' + (grid[column]) + " " * white_space + ' |\n'
            return text_lne

        output += top_line + empty_line
        for row in grid:
            output += text_line(grid.index(row))
        output += bottom_line
        return output

    return out_put_builder(grid_builder(card))


def display_deck(deck_dict):
    """Display all of the card pairs in the deck, separated by a '-->'."""
    printout = card_displayer("Question") + '   |\n   V' + card_displayer("Answer") + '\n'
    for item in deck_dict:
        printout += card_displayer(item['question']) + '   |\n   V' + card_displayer(item['answer']) + "\n"
    return printout

@app.route('/guess', methods=['GET', 'POST'])
def guess():
    guess = request.form.get('choice')
    f_b_pairs = session['f_b_pairs']
    random_pair = session['random_pair']
    
    answer = session['answer']
    del session['answer']
    if guess == answer:
        session['score'] += 1
        f_b_pairs.remove(random_pair)
        session['f_b_pairs'] = f_b_pairs
        return render_template('message2.html', message="Correct!", href="quiz_self")
    else:
        f_b_pairs.remove(random_pair)
        session['f_b_pairs'] = f_b_pairs
        return render_template('message2.html', message=f"Incorrect. The correct answer is：{card_displayer(answer)}", href="/quiz_self")
    
@app.route('/quiz_self', methods=['GET', 'POST'])
def quiz_self():
    f_b_pairs = session['f_b_pairs']
    # Front to back. Display front of card(key) in prompt, and answer must be its value
    if len(f_b_pairs) > 0:
        # From the tuple list, select a random index,
        random_pair = f_b_pairs[randrange(0, len(f_b_pairs))]
        session['random_pair'] = random_pair
        session['answer'] = random_pair['answer']
        return render_template('quiz.html', flashcard=random_pair)
    else :
        score = session['score']
        top_score = session['top_score']
        menu_choice = session['menu_choice']
        return render_template("message3.html", message=f"End of quiz. Your score was {str(round(100 * score / top_score, 2))}%. "
                f"You got {str(score)} out of {str(top_score)} questions correct.", href=f"/menu_choice/{menu_choice}")
        
@app.route('/answer', methods=['GET', 'POST'])
def answer():
    guess = request.form['guess']
    f_b_pairs = session['f_b_pairs']
    random_pair = session['random_pair']
    if guess == random_pair['answer']:
        session['score'] += 1
        f_b_pairs.remove(random_pair)
        session['f_b_pairs'] = f_b_pairs
        return render_template('message2.html', message="Correct!", href="/answer_quiz")
    else:
        f_b_pairs.remove(random_pair)
        session['f_b_pairs'] = f_b_pairs
        return render_template('message2.html', message=f"Incorrect. The correct answer is：{card_displayer(random_pair['answer'])}", href="/answer_quiz")

@app.route('/answer_quiz', methods=['GET', 'POST'])
def answer_quiz():
    f_b_pairs = session['f_b_pairs']
    score = session['score']
    top_score = session['top_score']
    if f_b_pairs:
        # From the tuple list, select a random index, and the 0th value of that (which is the card front)
        random_pair = f_b_pairs[randrange(0, len(f_b_pairs))]
        session['random_pair'] = random_pair
        return render_template("card_displayer_ans.html", data=card_displayer(random_pair['question']))
    else:
        menu_choice = session['menu_choice']
        return render_template("message3.html", message=f"End of quiz. Your score was {str(round(100 * score / top_score, 2))}%. "
          f"You got {str(score)} out of {str(top_score)} questions correct.", href=f"/menu_choice/{menu_choice}")
     
@app.route('/report_result', methods=['GET', 'POST'])
def report_result():
    correct_or_not = request.form['correct_or_not']
    f_b_pairs = session['f_b_pairs']
    random_pair = session['random_pair']
    if correct_or_not == "y":
        session['score'] += 1
        f_b_pairs.remove(random_pair)
        session['f_b_pairs'] = f_b_pairs
    elif correct_or_not == "n":
        f_b_pairs.remove(random_pair)
        session['f_b_pairs'] = f_b_pairs
    return report_quiz()

@app.route('/show_answer', methods=['GET', 'POST'])
def show_answer():
    random_pair = session['random_pair']
    data = card_displayer(random_pair['question']) + "\nThe answer is: {" + card_displayer(random_pair['answer']) + "} \nDid you guess correctly? \nAnswer y for yes and n for no: \n"
    return render_template("card_displayer_show_answer_review.html", data=data)
    
@app.route('/report_quiz', methods=['GET', 'POST'])
def report_quiz():
    f_b_pairs = session['f_b_pairs']
    score = session['score']
    top_score = session['top_score']
    
    # Front to back. Display front of card(key) in prompt, and answer must be its value
    if len(f_b_pairs) > 0:
        # From the tuple list, select a random index, and the 0th value of that (which is the card front)
        random_pair = f_b_pairs[randrange(0, len(f_b_pairs))]
        session['random_pair'] = random_pair
        return render_template("card_displayer_show_answer.html", data=card_displayer(random_pair['question']) + "Input any key to show answer:")
    else:
        menu_choice = session['menu_choice']
        return render_template("message3.html", message=f"End of quiz. Your score was {str(round(100 * score / top_score, 2))}%. "
            f"You got {str(score)} out of {str(top_score)} questions correct.", href=f"/menu_choice/{menu_choice}")

@app.route('/quiz_length', methods=['GET', 'POST'])
def quiz_length():
    quiz_length=request.form['quiz_length']
    deck_dict = get_deck()
    initial_pairs = [pair for pair in deck_dict]
    f_b_pairs = []
    while len(f_b_pairs) < int(quiz_length):
        quest_to_add = initial_pairs[randrange(len(initial_pairs))]
        if quest_to_add not in f_b_pairs:
            f_b_pairs.append(quest_to_add)
    session['score'] = 0
    session['top_score'] = len(f_b_pairs)
    session['f_b_pairs'] = f_b_pairs
    
    test_type = session['test_type']
    if test_type == 1:
        return quiz_self()
    elif test_type == 2:
        return answer_quiz()
    elif test_type == 3:
        return report_quiz()
    else:
        render_template('message.html', message="Invalid entry", goback=-1)
    
@app.route('/game_check', methods=['GET', 'POST'])  
def game_check():
    # Pick second card
    columns_count = session['columns_count']
    rows_count = session['rows_count']
    f_b_pairs1 = session['f_b_pairs1']
    choice1 = session['choice1']
    choice2 = request.form['choice2']
    choice1_picked = session['choice1_picked']
    grid = session['grid']
    incorrect = False
    if (choice2 == None or choice2 == "" or len(choice2) < 2):
        return render_template('message2.html', message="Incorrect input", href="/game_start")
    
    if choice2[0].isdigit() and choice2[1].isalpha():
        if len(choice2) == 2 and int(choice2[0]) <= rows_count and ord(choice2[1]) < columns_count + 97:
            choice2_picked = grid[int(choice2[0]) - 1][ord(choice2[1]) - 97]
            if choice2_picked != "0":
                session['choice2_picked'] = choice2_picked
            else:incorrect = True
        else: incorrect = True
    else: incorrect = True
    
    if incorrect == True:
        return render_template('message2.html', message="Incorrect input", href="/game_start")
                
    is_match = False
    print("-----------------")
    print(choice1_picked)
    print(choice2_picked)
    print("-----------------")
    for itm5 in f_b_pairs1:
        print(itm5)
        if choice1_picked in itm5 and choice2_picked in itm5:
            is_match = True

    print("-----------------")
    if is_match:
        message = "Congratulations! You found a match!"
        grid[int(choice1[0]) - 1][ord(choice1[1]) - 97] = "0"
        grid[int(choice2[0]) - 1][ord(choice2[1]) - 97] = "0"
    else:
        message = "Sorry, please try again."
    game_over = False
    for row in grid:
        for itm6 in row:
            if itm6 == "0":
                game_over = True
            else:
                game_over = False
    if game_over:
        game_round = session['game_round']
        deck_choice = session['deck_choice']
        
        del session['columns_count']
        del session['rows_count']
        del session['f_b_pairs1']
        del session['choice1']
        del session['choice1_picked']
        del session['grid']
        del session['game_round']
        del session['deck_choice']
        
        return render_template('message3.html', message=f"Congratulations, you won! It took you {str(game_round)} rounds.", href=f'/deck_choice/{deck_choice}')
    
    session['message'] = message
    return game_start()
       
@app.route('/game_play', methods=['GET', 'POST'])        
def game_play():
    columns_count = session['columns_count']
    rows_count = session['rows_count']
    choice1 = request.form['choice1']
    grid = session['grid']
    if (choice1 == None or choice1 == "" or len(choice1) < 2):
        return render_template('message2.html', message="Incorrect input", href="/game_start")
    if choice1[0].isdigit() and choice1[1].isalpha():
        if len(choice1) == 2 and int(choice1[0]) <= rows_count and ord(choice1[1]) < columns_count + 97:
            choice1_picked = grid[int(choice1[0]) - 1][ord(choice1[1]) - 97]
            if choice1_picked != "0":
                session['choice1_picked'] = choice1_picked
                session['choice1'] = choice1
                return render_template('game_check.html', grid=print_grid(grid), notice=card_displayer(choice1_picked), message="", value=choice1)
    
    return render_template('message2.html', message="Incorrect input", href="/game_start")

@app.route('/game_start', methods=['GET', 'POST'])
def game_start():
    grid = session['grid']
    game_round = session['game_round']
    game_over = session['game_over']
    message = ""
    if "message" in session:
        message = session["message"]
        del session["message"]
    if not game_over:
        session['game_round'] += 1
        # Pick first card
    return render_template("game_play.html", grid=print_grid(grid), notice=
f"\nPlease choose how many cards you'd like to include in the game, between 5 and 245\n"
f"Pick two cards. Try to find the pairs!\n"
f"When guessing, input row # and column letter\n"
f"eg. Row 3, Column b would be '3b'", message=message, value="")

def grid_maker(h, w):
    grid1 = [["0" for i in range(w)] for i in range(h)]
    return grid1

def print_grid(grid2): #-----
    print_gridb(grid2)
    y = 0
    columns_count = session['columns_count']
    message = "\n      columns\n      "
    for i in range(columns_count):
        # 'a' is ord(97), chr(97) is 'a'
        message += (str(chr(97 + y)) + "  ")
        y += 1
    message+="\n"
    x = 1
    for row1 in grid2:
        message += ("row " + str(x) + " ")
        x += 1
        for e in row1:
            # Print a blank if the card is empty, otherwise print a square
            if e == "0":
                message += "   "
            else:
                message += "口 "
        message+="\n"
    print(message)
    return message

def print_gridb(grid2):
    y = 0
    columns_count = session['columns_count']
    print("\n      columns\n      ", end="")
    for i in range(columns_count):
        # 'a' is ord(97), chr(97) is 'a'
        print(chr(97 + y), end="  ")
        y += 1
    print()
    x = 1
    for row1 in grid2:
        print("row " + str(x), end=" ")
        x += 1
        for e in row1:
            # Print a blank if the card is empty, otherwise print a square
            if e == "0":
                print("   ", end="")
            else:
                print("口 ", end="")
        print()
            
@app.route('/memory_game', methods=['GET', 'POST'])
def memory_game():
    """
    Plays a game of 'memory'

    :param deck_dict: a dictionary containing pairs of flashcards.
    """
    # Choose cards from deck
    # Converts dict into list of key/value tuples
    
    deck_dict = get_deck()
    
    initial_pairs0 = []
    for pair in deck_dict:
        initial_pairs0.append((pair['question'], pair['answer']))
    initial_pairs = [[i for i in pair] for pair in initial_pairs0]
    print(initial_pairs)
    # Make user choose quiz length
    length_chosen = False
    if not length_chosen:
        game_length = request.form['cards_count']
        if game_length.isdigit():
            if 24 >= int(game_length) >= 5 and int(game_length) < len(initial_pairs):
                session['game_length'] = game_length
            else:
                return render_template("memory_game.html", title="Memory Game:pairs less or cards less")
        else:
            return render_template("memory_game.html", title="Memory Game:Please pick again")
    # Add as many questions to the quiz as the user had specified
    f_b_pairs = []
    while len(f_b_pairs) < int(game_length):
        quest_to_add = initial_pairs[randrange(len(initial_pairs))]
        if quest_to_add not in f_b_pairs:
            f_b_pairs.append(quest_to_add)
    # Calculate the board size
    # Columns_count will be width, rows_count height
    columns_count = math.floor(math.sqrt(int(game_length) * 2)) #-----
    rows_count = math.ceil((int(game_length) * 2) / columns_count) #-----
    # Because we pop out elements of the list when filling the grid, we need to copy for later reference.
    f_b_pairs1 = copy.deepcopy(f_b_pairs)

    grid = grid_maker(rows_count, columns_count) #-----
    # Fill grid, make sure the target location is empty ("0"), pop the itm and fill till each item in the list is empty
    for itm4 in f_b_pairs:
        while len(itm4) > 0:
            target_row = randrange(rows_count)
            target_col = randrange(columns_count)
            target = grid[target_row][target_col]
            if target == "0":
                grid[target_row][target_col] = itm4.pop()

    # Start the game here
    print("Pick two cards. Try to find the pairs!\nWhen guessing, input row # and column letter"
          "\neg. Row 3, Column b would be '3b' ")
    game_round = 0 #-----
    game_over = False
    session['columns_count'] = columns_count
    session['rows_count'] = rows_count
    session['grid'] = grid
    session['game_round'] = game_round
    session['game_over'] = game_over
    session['f_b_pairs1'] = f_b_pairs1
    return game_start()

@app.route('/add_to_base', methods=['POST'])
def add_to_base():
    flashcards = load_flashcards('flashcards(chinese elements).csv')
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
        
@app.route('/main')
def main():
    if not session['username']:
        return redirect(url_for('signin'))
    # Find all json files in local directory, decks will be a list of their paths
    decks = glob.glob(program_directory() + "/*.csv")
    numbered_paths_and_names = deck_menu_constructor(decks)
    # makes a variable to hold the list of deck names with a given number starting at 1
    decks_choice_display = []
    for name_path_tup in numbered_paths_and_names:
        if str(name_path_tup[1]) != 'users':
            decks_choice_display.append({'id': str(name_path_tup[0]), 'name': str(name_path_tup[1])})

    # Deck choice menu prompt
    session['deck_chosen'] = False
    return render_template('main.html', decks_choice_display = decks_choice_display)

@app.route('/deck_choice/<int:deck_choice>')
def deck_choice(deck_choice):
    session['deck_choice'] = deck_choice
    return render_template('deck_choice.html')
    
@app.route('/add_item', methods=['GET', 'POST'])
def add_item():
    deck = get_deck()
    new_item_front = request.form['question']
    new_item_back = request.form['answer']
    choices = request.form.getlist('choices')
    file = request.files['file']
    choices.insert(randrange(0, 4), new_item_back)
    if new_item_front == None or new_item_back == None or new_item_front == '' or choices == None:
        return render_template('message.html', message="Input empty!", goback=-1)
    
    inDeck = False
    for item in deck:
        if new_item_front == item['question']:
            inDeck = True
            break
    
    if inDeck == False:
        if file and allowed_file(file.filename):
            file_name = file.filename
            file_type = file_name.split('.')[-1]
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
            save_flashcard(new_item_front, new_item_back, choices, file_type, file_name, session['filename'])
        else:
            save_flashcard(new_item_front, new_item_back, choices, '', '', session['filename'])
        message="Added successfully!"
    else:
        message="Word already in deck"
        
    return render_template('message.html', message=message, goback=-2)
        
@app.route('/remove_item', methods=['GET', 'POST'])
def remove_item():
    remove = request.form['remove']
    deck = get_deck()
    answer = ''
    isFound = False
    for d in deck:
        if d['question'] == remove:
            isFound = True
            answer = d['answer']
            break
        
    if isFound:
        message="Removed {" + remove + "} ---> {" + answer + "}"
        del_flashcard(remove, session['filename'])
    else:
        message="Word not in deck"
        
    return render_template('message.html', message=message, goback=-2)

@app.route('/front_to_back_prompt/<string:direction>')
def front_to_back_prompt(direction):
    session['direction'] = direction
    if direction == "f" or direction == "b":
        return render_template('quiz_length.html')
    else:
        return render_template('message.html', message="Invalid entry", goback=-1)        
            
@app.route('/quiz_yourself/<int:test_type>')
def quiz_yourself(test_type):
    
    session['test_type'] = test_type
    # return render_template('front_to_back_prompt.html')
    return render_template('quiz_length.html')

@app.route('/confirm_override', methods=['GET', 'POST'])
def confirm_override():
    
    txts = glob.glob(program_directory() + "/*.txt")
    numbered_paths_and_names1 = deck_menu_constructor(txts)
    
    file_choice = session['file_choice']
    overwrite = request.form['overwrite']
    
    if overwrite == "y":
        print("Importing...")
        import_quizlet_lineskip_fix(numbered_paths_and_names1[int(file_choice) - 1][2])
        return render_template('message2.html', message="Success!", href=f"/deck_choice/{deck_choice}")
    else:
        return render_template('message2.html', message="Canceled!", href=f"/deck_choice/{deck_choice}")
    
@app.route('/separator_select', methods=['GET', 'POST'])
def separator_select():
    
    txts = glob.glob(program_directory() + "/*.txt")
    numbered_paths_and_names1 = deck_menu_constructor(txts)
    
    ask_fbsep = request.form['ask_fbsep']
    ask_cardsep = request.form['ask_cardsep']
    
    file_choice = session['file_choice']
    
    print("Importing...")
    import_quizlet_lineskip_fix(numbered_paths_and_names1[int(file_choice) - 1][2],
                                fbsep=ask_fbsep, cardsep=ask_cardsep)
    return render_template('message2.html', message="Success!", href=f"/deck_choice/{deck_choice}")

@app.route('/confirm_exist', methods=['GET', 'POST'])
def confirm_exist():
    
    txts = glob.glob(program_directory() + "/*.txt")
    numbered_paths_and_names1 = deck_menu_constructor(txts)
    
    file_choice = session['file_choice']
    
    is_default = request.form['is_default']
    if is_default == "y":
        # The number the user enters will be 1 more than the index for the
        # tuple where the path is the 2th entry
        if numbered_paths_and_names1[int(file_choice) - 1][2] in program_directory():
            return render_template('check_exist.html')
        else:
            import_quizlet_lineskip_fix(numbered_paths_and_names1[int(file_choice) - 1][2])
            return render_template('message2.html', message="Success!", href=f"/deck_choice/{deck_choice}")
    else:
        return render_template('separator_select.html')
    
@app.route('/check_default', methods=['GET', 'POST'])
def check_default():
    
    file_choice = request.form['file_choice']
    is_quizlet = request.form['is_quizlet']
    session['file_choice'] = file_choice
    session['is_quizlet'] = is_quizlet
    if is_quizlet == "y":
        return render_template("check_default.html")
    else:
        deck_choice = session['deck_choice']
        return render_template('message2.html', message="Unsupported file type.", href=f"/deck_choice/{deck_choice}")

def choose_file():
    # Find all txt files in local directory, txts variable will be a list of their paths
    txts = glob.glob(program_directory() + "/*.txt")
    numbered_paths_and_names1 = deck_menu_constructor(txts)
    return render_template('choose_file.html', numbered_paths_and_names1=numbered_paths_and_names1)

@app.route('/menu_choice/<int:menu_choice>')
def menu_choice(menu_choice):
    session['menu_choice'] = menu_choice
    deck = get_deck()
    if menu_choice == 1:
        return render_template("menu_choice1.html", printout=display_deck(deck))
    elif menu_choice == 2:
        return render_template("add_item.html")
    elif menu_choice == 3:
        return render_template("remove_item.html")
    elif menu_choice == 4:
        return render_template("quiz_yourself.html", href=f"/deck_choice/{session['deck_choice']}")
    elif menu_choice == 5:
        return render_template("memory_game.html", title="Memory Game")
    elif menu_choice == 6:
        return main()
    elif menu_choice == 7:
        return choose_file()

if __name__ == '__main__':
    app.run(debug=True)
    
