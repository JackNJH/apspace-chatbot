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
6. Train the bot with `rasa train` to get the first 'model'. 
7. Type `rasa shell` in the terminal to run the chatbot.

## How to Save Changes Made to the Bot:
You should train the bot after making any changes.
1. Type `rasa train` in the terminal to train the chatbot.
2. Type `rasa run actions` if you have any custom actions.
3. Continue with `rasa shell` in the terminal to run the chatbot.


### Files and Details:

| File         | Details                                      |
| ------------ | -------------------------------------------- |
| `nlu.yml`     | Give example user messages to train the NLU model. |
| `domain.yml`  | The brain of the chatbot. All intents, responses, etc. should be registered in this file. |
| `stories.yml`  | Like a decision-based story game, the different paths that a conversation can take are captured here. |
| `rules.yml`  | Explicit rules or conditions to handle specific user inputs are defined here.  |
| models  | Each time you train the bot it creates a new 'model' in the models folder. |
