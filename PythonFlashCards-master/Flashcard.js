const deck = {"fire": "火 huo3",
        "water": "水 shui3",
        "earth": "土 tu3",
        "air": "气 qi4",
        }


const print_deck = (deck_dict) => {
    let printout = "Front --> Back:\n\n"
    Object.keys(deck_dict).map((item) => {
        printout += item + " --> " + deck_dict[item] + "\n"
    })
    return printout
}
    

const welcome = `
      Welcome to
      
^_^   Flashcards   ^_^
`

const menu = `\nmenu:

\n1. View deck
\n2. Add item
\n3. Delete item
\n4. Quiz yourself
\n5. Quit

\nYour choice: `

const test_type_prompt = `\nPlease choose quiz type:

1. Multiple choice
2. Write the answer
3. Self report

Your choice: `

const front_to_back_prompt = `\nPlease choose whether you'd like to be presented with 
the front and guess the back, or vice versa:

f. See front, guess back
b. See back, guess front

your choice:`

let welcomeArea = document.getElementById("welcome")
welcomeArea.innerHTML = welcome
let displayArea = document.getElementById("display")
displayArea.innerHTML = menu
let outcomeArea = document.getElementById("outcome")
let menuInput = document.getElementById("menu-input")
let nemuSubmit = document.getElementById("menu-submit")
nemuSubmit.onclick = () => {
    const menuChoice = menuInput.value
    outcomeArea.innerHTML = ""
    if (menuChoice === "1") {
        let currentDeck = document.createElement('div')
        currentDeck.innerHTML = "\n" + "Current deck:\n" + print_deck(deck), "\n"
        outcomeArea.appendChild(currentDeck)
    } else if (menuChoice === "2") {
        let front = document.createElement('input')
        let back = document.createElement('input')
        let itemSubmit = document.createElement('button')

        itemSubmit.innerHTML = "Add item"

        itemSubmit.onclick = (e) => {
            let [key, value, _] = e.target.parentElement.children
            let result = document.createElement('div')
            if (!Object.keys(deck).includes(key.value)){
                deck[key.value] = value.value
                result.innerHTML = "Added successfully!"
            } else {
                result.innerHTML = "Word already in deck"
            }
            outcomeArea.appendChild(result)
        }

        outcomeArea.appendChild(front)
        outcomeArea.appendChild(back)
        outcomeArea.appendChild(itemSubmit)

    } else if (menuChoice === "3") {
        
    } else if (menuChoice === "4") {
        
    } else if (menuChoice === "5") {
        
    } else {
        console.log("invalid input")
    }
}
