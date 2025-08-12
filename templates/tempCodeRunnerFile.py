from flask import Flask, render_template, request
from spellchecker import SpellChecker

# Initialize Flask app and spell checker
app = Flask(__name__)
spell = SpellChecker()

@app.route('/', methods=['GET', 'POST'])
def index():
    corrected_text = ""  # Will hold the corrected output

    if request.method == 'POST':
        input_text = request.form['text']  # Get text from form
        words = input_text.split()
        corrected_words = []

        # Check and correct each word
        for word in words:
            # If word is known, keep it; else correct it
            if word.lower() in spell:
                corrected_words.append(word)
            else:
                correction = spell.correction(word)
                corrected_words.append(correction if correction else word)

        # Join corrected words back into a sentence
        corrected_text = ' '.join(corrected_words)

    return render_template('index.html', corrected=corrected_text)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)