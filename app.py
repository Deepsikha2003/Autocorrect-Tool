from flask import Flask, render_template, request
import language_tool_python

app = Flask(__name__)
tool = language_tool_python.LanguageTool('en-US')

@app.route('/', methods=['GET', 'POST'])
def index():
    corrected_text = ""
    suggestions = []

    if request.method == 'POST':
        input_text = request.form['text']
        matches = tool.check(input_text)

        corrected_text = language_tool_python.utils.correct(input_text, matches)

        for match in matches:
            context_text = ""
            context_offset = 0

            # --- CHANGE HERE: Robustly get suggestion_length ---
            suggestion_length = 0 # Default value
            if hasattr(match, 'length') and match.length is not None:
                suggestion_length = match.length
            # --------------------------------------------------

            if match.context:
                if hasattr(match.context, 'text') and match.context.text:
                    context_text = match.context.text
                if hasattr(match.context, 'offset') and match.context.offset is not None:
                    context_offset = match.context.offset

            wrong_word_snippet = ""
            try:
                if context_text and context_offset is not None and suggestion_length > 0 and \
                   context_offset + suggestion_length <= len(input_text):
                    if input_text[context_offset:context_offset + suggestion_length] == context_text[0:suggestion_length]:
                         wrong_word_snippet = input_text[context_offset:context_offset + suggestion_length]
                    else:
                         wrong_word_snippet = context_text[0:suggestion_length]
                elif suggestion_length > 0 and hasattr(match, 'offset') and match.offset is not None and match.offset + suggestion_length <= len(input_text):
                     # Use match.offset directly if context is problematic, but ensure it exists
                     wrong_word_snippet = input_text[match.offset:match.offset + suggestion_length]
                else:
                    if match.replacements and match.replacements[0]:
                        wrong_word_snippet = f"'{match.replacements[0]}' (approx.)"
                    else:
                        wrong_word_snippet = "(Unknown)"

            except IndexError:
                wrong_word_snippet = "(Error extracting)"
            except TypeError:
                wrong_word_snippet = "(Invalid data)"

            suggestions.append({
                "message": match.message,
                "replacements": match.replacements,
                "wrong_word_display": wrong_word_snippet,
                "raw_context": match.context
            })

    return render_template('index.html', corrected=corrected_text, suggestions=suggestions)

if __name__ == '__main__':
    app.run(debug=True)