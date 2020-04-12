from pathlib import Path
Path("feedback").mkdir(parents=True, exist_ok=True)

def process_feedback(text):
    with open("feedback/feedback.txt", 'a+') as file:
        file.write('==============================================\n')
        file.write(text)
        file.write('\n\n')

def process_unfound_item(text):
    with open("feedback/suggested_items.txt", 'a+') as file:
        file.write('==============================================\n')
        file.write(text)
        file.write('\n\n')





