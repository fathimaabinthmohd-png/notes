import unittest

from app import app, db, Note


class TravelAppTests(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.client = app.test_client()
        with app.app_context():
            db.create_all()
            # Ensure a clean database
            Note.query.delete()
            db.session.commit()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_edit_note_updates_selected_note(self):
        with app.app_context():
            n = Note(content="First note")
            db.session.add(n)
            db.session.commit()
            note_id = n.id

        response = self.client.post(
            f"/edit/{note_id}",
            data={"content": "Updated note"},
            follow_redirects=True,
        )

        self.assertEqual(response.status_code, 200)
        with app.app_context():
            n = Note.query.get(note_id)
            self.assertIsNotNone(n)
            self.assertEqual(n.content, "Updated note")
        self.assertIn("Updated note", response.get_data(as_text=True))

    def test_delete_note_removes_only_selected_note(self):
        with app.app_context():
            n1 = Note(content="Keep me")
            n2 = Note(content="Delete me")
            db.session.add_all([n1, n2])
            db.session.commit()
            id_keep = n1.id
            id_delete = n2.id

        response = self.client.post(f"/delete/{id_delete}", follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        with app.app_context():
            remaining = Note.query.all()
            self.assertEqual(len(remaining), 1)
            self.assertEqual(remaining[0].content, "Keep me")
        self.assertNotIn("Delete me", response.get_data(as_text=True))


if __name__ == "__main__":
    unittest.main()
