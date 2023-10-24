# Falshcard
## About the project
This is the project for University of Melbourne IT Project(COMP30022_2023_SM2)
The purpose of this project is to realize the flashcard system of C-LARA platform, including user login, create flashcard, delete flashcard, use flashcard to answer questions and other functions.
## User Stories：
    Google drive：https://drive.google.com/drive/folders/1-2aZ1leEu6sYL7WKsT80ouxS-IgTI0i7?
## Prepare
This flashcard run based on html and python (under version 3.11.5, not test under ohter situation), so only need to constrct all environment for python and html, then download all files. We use csv, flask, pandas, please make sure your editor can use and read the above functions or frameworks. The functions and logic of Flashcard are in the app.py file in the Flashcard folder. The web page code is also in the tamplate folder of the Flahcard folder. The back-end language is Python, and there is no too profound logic. Some function codes contain comments (in Chinese or English).

## How to run
download all files and run app.py will apply adress.
## Features that have been implemented and tested
### log in and log up
### Flashcard deck selection
### View item 
    View questions and answers from the selected deck
### Add item ——— Add answers and options
    * Update：* 1.Multimedia (images, audio (mp3 files) and video (mp4)) files can now be added when adding questions, answers and options.
              * 2.Added multimedia displays successfully with the question (tested)
### Quiz yoursefl ——— Multiple choice questions（flashcard main question types）
                 * Answer question（More diverse question types envisioned for the future）
                 * Self report（More diverse question types envisioned for the future）
                 * Update： To add feedback functions and reports after answering questions, for example:
                           After completing a question and submitting a wrong answer, the correct answer will be displayed and a countdown will begin. When the countdown ends, it will enter the next                             question. 
                           After completing all questions, the correct rate will be displayed as a score.
### Play a game—— A simple memory game based on the flashcard function (the main purpose is to design some interesting games to help users learn in the future)
## API
Most of the API work is complete and the web code can be found in the tamplate in the Flashcard folder.
## UI design
* Most of the web pages and Flahcard UI have been completed, and the specific effects can be found on Google drive: https://drive.google.com/drive/folders/1-2aZ1leEu6sYL7WKsT80ouxS-IgTI0i7? 
  usp=sharing
  Additional information—— There are no web pages with UI design added to Flashcard and the reasons are as follows:
                          1. View deck
                          2. Quiz yourself—answer quiz and Self report
                          3. Play a game
                          Reason：The existing questions and answers are directly displayed in the view deck. Due to time and scheduling issues, no UI design is added. There are separate web pages                             in the tamplate folder that can be changed. The reason why there is no UI design for the other two question types and game functions except the multiple-choice questions is                           because these three functions are not the main required functions, so this is a reference and case provided for future design. The above functions have not been added with                            UI design due to time or other reasons, but the functions have been implemented. If there is free time, we will consider adding UI design.

## Test
    Google drive：https://drive.google.com/drive/folders/1-2aZ1leEu6sYL7WKsT80ouxS-IgTI0i7?
