import unittest

from app import app, db, Note, NoteLine


class TravelAppTests(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.client = app.test_client()
        with app.app_context():
            # Recreate schema to match current models
            db.drop_all()
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_edit_note_updates_selected_note(self):
        with app.app_context():
            n = Note(heading="Test")
            db.session.add(n)
            db.session.flush()
            ln = NoteLine(note_id=n.id, content="First note", position=0)
            db.session.add(ln)
            db.session.commit()
            note_id = n.id

        response = self.client.post(
            f"/edit/{note_id}",
            data={"lines[]": "Updated note", "heading": "Test"},
            follow_redirects=True,
        )

        self.assertEqual(response.status_code, 200)
        with app.app_context():
            lines = NoteLine.query.filter_by(note_id=note_id).all()
            self.assertEqual(len(lines), 1)
            self.assertEqual(lines[0].content, "Updated note")
        self.assertIn("Updated note", response.get_data(as_text=True))

    def test_delete_note_removes_only_selected_note(self):
        with app.app_context():
            n1 = Note(heading="A")
            n2 = Note(heading="B")
            db.session.add_all([n1, n2])
            db.session.flush()
            l1 = NoteLine(note_id=n1.id, content="Keep me", position=0)
            l2 = NoteLine(note_id=n2.id, content="Delete me", position=0)
            db.session.add_all([l1, l2])
            db.session.commit()
            id_keep = n1.id
            id_delete = n2.id

        response = self.client.post(f"/delete/{id_delete}", follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        with app.app_context():
            remaining_notes = Note.query.all()
            self.assertEqual(len(remaining_notes), 1)
            remaining_lines = NoteLine.query.filter_by(note_id=remaining_notes[0].id).all()
            self.assertEqual(len(remaining_lines), 1)
            self.assertEqual(remaining_lines[0].content, "Keep me")
        self.assertNotIn("Delete me", response.get_data(as_text=True))


if __name__ == "__main__":
    unittest.main()
