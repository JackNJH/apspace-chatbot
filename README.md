# IAI Group 12

Group 12's AI Chatbot Assignment. Instructions are provided below.

## How to Setup in VSCode:

1. Download the code (Or collaborate on Git directly if you know how).
2. Have Python's extension installed in VSCode under 'Extensions'.
3. Open the file in VSCode's integrated terminal.
4. Set up a Virtual Environment (Optional but Recommended):
   - Open terminal in the project directory.
   - Run the command: `python -m venv venv`
   - Activate the virtual environment with `venv\Scripts\activate` (or `source venv/bin/activate` on Linux/Mac).
   - With the virtual environment activated, install dependencies: `pip install rasa`.
5. Type `rasa shell` in the terminal to run the chatbot.

## How to Train the Bot:

1. Download the code (Or collaborate on Git directly if you know how).

### Files and Details:

| File         | Details                                      |
| ------------ | -------------------------------------------- |
| nlu.yml      | Give example user messages to train the NLU model. |
| domain.yml   | The brain of the chatbot. All intents, responses, etc. should be registered in this file. |
| stories.yml  | Like a decision-based story game, the responses of the chatbot which are guided by the user's input are created here. |
