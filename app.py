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
    heading = db.Column(db.String(200), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Note {self.id}: {self.heading or self.id}>"


class NoteLine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    note_id = db.Column(db.Integer, db.ForeignKey('note.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    position = db.Column(db.Integer, nullable=False, default=0)
    is_point = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    note = db.relationship('Note', backref=db.backref('lines', cascade='all, delete-orphan', order_by='NoteLine.position'))

    def __repr__(self):
        return f"<Line {self.id} (Note {self.note_id}): {self.content[:20]}>"
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
        heading = request.form.get('heading', '').strip()
        # support both names: lines[] or lines
        lines = request.form.getlist('lines[]') or request.form.getlist('lines')
        points = request.form.getlist('points[]') or request.form.getlist('points')
        if lines:
            n = Note(heading=heading or None)
            db.session.add(n)
            db.session.flush()
            for i, text in enumerate(lines):
                text = (text or '').strip()
                if not text:
                    continue
                is_point = False
                try:
                    is_point = (points[i] == 'on')
                except Exception:
                    is_point = False
                ln = NoteLine(note_id=n.id, content=text, position=i, is_point=is_point)
                db.session.add(ln)
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
        heading = request.form.get('heading', '').strip()
        lines = request.form.getlist('lines[]') or request.form.getlist('lines')
        points = request.form.getlist('points[]') or request.form.getlist('points')
        note.heading = heading or None
        # replace existing lines
        NoteLine.query.filter_by(note_id=note.id).delete()
        db.session.flush()
        for i, text in enumerate(lines):
            text = (text or '').strip()
            if not text:
                continue
            is_point = False
            try:
                is_point = (points[i] == 'on')
            except Exception:
                is_point = False
            ln = NoteLine(note_id=note.id, content=text, position=i, is_point=is_point)
            db.session.add(ln)
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


@app.route('/delete_line/<int:line_id>', methods=['POST'])
def delete_line(line_id):
    ln = NoteLine.query.get(line_id)
    note_id = None
    if ln:
        note_id = ln.note_id
        db.session.delete(ln)
        db.session.commit()
    if note_id:
        return redirect(url_for('edit_note', note_id=note_id))
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)