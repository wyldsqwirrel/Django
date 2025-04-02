# core/tests.py
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Task, Email, Board, BoardItem, Note

class TaskTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.task = Task.objects.create(
            user=self.user,
            title='Test Task',
            description='Test Description',
            due_date='2025-01-01T12:00:00Z'
        )
        self.email = Email.objects.create(
            user=self.user,
            subject='Test Email',
            sender='sender@example.com'
        )

    def test_task_creation(self):
        self.assertEqual(self.task.title, 'Test Task')

    def test_email_creation(self):
        self.assertEqual(self.email.subject, 'Test Email')

class ProductivityTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.board = Board.objects.create(user=self.user, title='Test Board')
        self.board_item = BoardItem.objects.create(board=self.board, content='Test Item')
        self.note = Note.objects.create(user=self.user, title='Test Note', content='Test Content')

    def test_board_creation(self):
        self.assertEqual(self.board.title, 'Test Board')

    def test_board_item_creation(self):
        self.assertEqual(self.board_item.content, 'Test Item')

    def test_note_creation(self):
        self.assertEqual(self.note.title, 'Test Note')
