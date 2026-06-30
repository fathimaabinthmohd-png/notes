import unittest

from app import app, notes


class TravelAppTests(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.client = app.test_client()
        notes.clear()

    def test_edit_note_updates_selected_note(self):
        notes.append({"content": "First note", "created_at": "2026-06-30 10:00:00", "updated_at": "2026-06-30 10:00:00"})

        response = self.client.post(
            "/edit/0",
            data={"content": "Updated note"},
            follow_redirects=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(notes[0]["content"], "Updated note")
        self.assertIn("Updated note", response.get_data(as_text=True))

    def test_delete_note_removes_only_selected_note(self):
        notes.extend([
            {"content": "Keep me", "created_at": "2026-06-30 10:00:00", "updated_at": "2026-06-30 10:00:00"},
            {"content": "Delete me", "created_at": "2026-06-30 10:05:00", "updated_at": "2026-06-30 10:05:00"},
        ])

        response = self.client.post("/delete/1", follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(notes), 1)
        self.assertEqual(notes[0]["content"], "Keep me")
        self.assertNotIn("Delete me", response.get_data(as_text=True))


if __name__ == "__main__":
    unittest.main()
