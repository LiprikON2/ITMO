from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model
import datetime

from notes.models import Note

User = get_user_model()


class NoteModelTests(TestCase):

    def setUp(self):
        self.test_user = User.objects.create_user(
            email="test_user@example.com",
            password="secret")
    
    def test_can_create_a_new_note(self):
        note = Note.objects.create(title='Note title', body='Note body', owner=self.test_user)
        self.assertTrue(note)

    def test_string_representation(self):
        note = Note.objects.create(title='Note title', body='Note body', owner=self.test_user)
        self.assertEqual(str(note), 'Note title')

    def test_was_published_recently_with_future_note(self):
        """
        was_published_recently() returns False for notes whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_note = Note(pub_date=time)
        self.assertIs(future_note.was_published_recently(), False)
        
    def test_was_published_recently_with_old_note(self):
        """
        was_published_recently() returns False for notes whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_note = Note(pub_date=time)
        self.assertIs(old_note.was_published_recently(), False)

    def test_was_published_recently_with_recent_note(self):
        """
        was_published_recently() returns True for notes whose pub_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_note = Note(pub_date=time)
        self.assertIs(recent_note.was_published_recently(), True)

    def test_can_create_note_with_tags(self):
        pass
    
    