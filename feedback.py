from pathlib import Path


def process_feedback(text):
    Path("feedback").mkdir(parents=True, exist_ok=True)
    with open("feedback/feedback.txt", 'a+') as file:
        file.write('==============================================\n')
        file.write(text)
        file.write('\n\n')

def process_unfound_item(text):
    Path("feedback").mkdir(parents=True, exist_ok=True)
    with open("feedback/suggested_items.txt", 'a+') as file:
        file.write('==============================================\n')
        file.write(text)
        file.write('\n\n')

def process_happy_feedback():
    Path("feedback").mkdir(parents=True, exist_ok=True)
    with open("feedback/happy.txt", 'a+') as file:
        file.write('happy\n')

def process_sad_feedback():
    Path("feedback").mkdir(parents=True, exist_ok=True)
    with open("feedback/sad.txt", 'a+') as file:
        file.write('sad\n')




