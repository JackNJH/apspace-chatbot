# IAI Group 12

Group 12's AI Chatbot for APSpace using Rasa AI. Instructions are provided below.  
**RASA ONLY WORKS ON PYTHON 3.7, 3.8, 3.9, 3.10**

## How to Setup in VSCode:

1. Download the code (Or collaborate on Git directly if you know how).
2. Have Python's extension installed in VSCode under 'Extensions'.
3. Open the file in VSCode's integrated terminal (**Make sure the correct directory is selected**). 
4. Set up a Virtual Environment (Optional but Recommended):
   - Open terminal in the project directory.
   - Run the command: `python -m venv venv`.
   - Activate the virtual environment with `venv\Scripts\activate` (or `source venv/bin/activate` on Linux/Mac).
   - With the virtual environment activated, install dependencies: `pip install rasa`.
5. This is an example of how the terminal should look like in venv.
   ![Example Image](images/example.png)
6. Type `rasa run actions` to run custom actions. Leave this terminal open, and open a new terminal.
7. Train the bot with `rasa train` in the new terminal to get the first 'model'. 
8. Type `rasa shell` in the terminal to run the chatbot.

## How to Save Changes Made to the Bot:
You should train the bot after making any changes.
1. Type `rasa train` in the terminal to train the chatbot.
2. Type `rasa run actions` to restart the server if you have many any changes to `actions.py`.
3. Continue with `rasa shell` in the terminal to run the chatbot.


### Files and Description:

| File         | Description                                      |
| ------------ | -------------------------------------------- |
| `nlu`         | Contains example user messages to train the NLU model. Intents and synonyms should be defined here.  |
| `domain.yml`  | The brain of the chatbot. All intents, actions, slots, entities, etc. should be registered in this file. |
| `stories`     | Captures different paths that a conversation can take, similar to a decision-based story game. |
| `rules.yml`   | Explicit rules or conditions to handle specific user inputs are defined here.  |
| `models`      | Each time you train the bot, it creates a new 'model' in the models folder. |
| `actions.py`  | Custom actions for the bot to execute. Any complex responses that require fetching from the database are defined here. |
| `database`    | Database file. Create and store all your mock data here. |

### Terms and Description:

| Term        | Description                                 |
| ----------- | ------------------------------------------- |
| Intents     | Used to sample example user inputs so the bot can recognize the user's intent and decide the next action. |
| Slots       | Used to store and retrieve information from the user's input. They represent pieces of data that the chatbot needs to keep track of during a conversation. |
| Entities    | Specific pieces of information that the chatbot extracts from user messages. These are the 'key terms' the bot searches for in an intent. |



