"""
Flask Tutorial App for Students
--------------------------------
This file demonstrates a basic Flask web application.
Students can learn about routes, templates, and handling forms.
"""

from datetime import datetime

from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)

# In-memory storage for demonstration (not for production use)
notes = []


def now_string():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


@app.route('/')
def index():
    """Home page showing a welcome message and list of notes."""
    return render_template('index.html', notes=notes)


@app.route('/add', methods=['GET', 'POST'])
def add_note():
    """Handle adding a new note via a form."""
    if request.method == 'POST':
        note_content = request.form.get('content', '').strip()
        if note_content:
            notes.append({
                'content': note_content,
                'created_at': now_string(),
                'updated_at': now_string(),
            })
        return redirect(url_for('index'))
    return render_template('add.html')


@app.route('/edit/<int:note_id>', methods=['GET', 'POST'])
def edit_note(note_id):
    """Edit a single note by its index."""
    global notes
    if not 0 <= note_id < len(notes):
        return redirect(url_for('index'))

    if request.method == 'POST':
        new_content = request.form.get('content', '').strip()
        if new_content:
            notes[note_id]['content'] = new_content
            notes[note_id]['updated_at'] = now_string()
        return redirect(url_for('index'))

    return render_template('add.html', note=notes[note_id], edit=True, note_id=note_id)


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
    app.run(debug=True)