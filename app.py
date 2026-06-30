"""Flask Tutorial App with SQLite persistence
-------------------------------------------
This app demonstrates a small CRUD web application using Flask and
Flask-SQLAlchemy so notes persist between restarts. It keeps the same
simple routes and templates but stores data in `app.db`.
"""

from datetime import datetime

from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Note {self.id}: {self.content[:20]}>"

with app.app_context():
    db.create_all()


@app.route('/')
def index():
    """Home page showing a welcome message and list of notes."""
    notes = Note.query.order_by(Note.created_at.desc()).all()
    return render_template('index.html', notes=notes)


@app.route('/add', methods=['GET', 'POST'])
def add_note():
    """Handle adding a new note via a form."""
    if request.method == 'POST':
        note_content = request.form.get('content', '').strip()
        if note_content:
            n = Note(content=note_content)
            db.session.add(n)
            db.session.commit()
        return redirect(url_for('index'))
    return render_template('add.html')


@app.route('/edit/<int:note_id>', methods=['GET', 'POST'])
def edit_note(note_id):
    """Edit a single note by id."""
    note = Note.query.get(note_id)
    if note is None:
        return redirect(url_for('index'))

    if request.method == 'POST':
        new_content = request.form.get('content', '').strip()
        if new_content:
            note.content = new_content
            note.updated_at = datetime.utcnow()
            db.session.commit()
        return redirect(url_for('index'))

    return render_template('add.html', note=note, edit=True)


@app.route('/delete/<int:note_id>', methods=['POST'])
def delete_note(note_id):
    """Delete a single note by its id."""
    note = Note.query.get(note_id)
    if note:
        db.session.delete(note)
        db.session.commit()
    return redirect(url_for('index'))


@app.route('/clear')
def clear_notes():
    """Clear all notes from the database."""
    Note.query.delete()
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)