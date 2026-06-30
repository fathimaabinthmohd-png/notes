"""
Flask Tutorial App for Students
--------------------------------
This file demonstrates a basic Flask web application.
Students can learn about routes, templates, and handling forms.
"""

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# In-memory storage for demonstration (not for production use)
notes = []

@app.route('/')
def index():
    """Home page showing a welcome message and list of notes."""
    return render_template('index.html', notes=notes)

@app.route('/add', methods=['GET', 'POST'])
def add_note():
    """Handle adding a new note via a form."""
    if request.method == 'POST':
        note_content = request.form.get('content')
        if note_content:
            notes.append(note_content)
        return redirect(url_for('index'))
    # GET request: show the form
    return render_template('add.html')

@app.route('/delete/<int:note_id>', methods=['POST'])
def delete_note(note_id):
    """Delete a single note by its index."""
    global notes
    if 0 <= note_id < len(notes):
        notes.pop(note_id)
    return redirect(url_for('index'))

@app.route('/clear')
def clear_notes():
    """Clear all notes."""
    global notes
    notes = []
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Run the app in debug mode for development
    app.run(debug=True)