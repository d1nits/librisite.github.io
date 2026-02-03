from django.test import TestCase
from django.contrib.auth.models import User

from user.models import Profile
from .models import Book, Review, Category, Tag, ReviewTag



class BookModelTest(TestCase):
    def setUp(self):
        self.book = Book.objects.create(
            title='Test Book',
            author='Test Author'
        )

    def test_book_str(self):
        self.assertEqual(str(self.book), 'Test Book')


class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name='Test Category'
        )

    def test_category_str(self):
        self.assertEqual(str(self.category), 'Test Category')




class TagModelTest(TestCase):
    def setUp(self):
        self.tag = Tag.objects.create(
            name='Test Tag'
        )

    def test_tag_str(self):
        self.assertEqual(str(self.tag), 'Test Tag')



class ReviewModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.profile = Profile.objects.create(user=self.user)

        self.book = Book.objects.create(
            title='Test Book',
            author='Test Author'
        )

        self.review = Review.objects.create(
            book=self.book,
            author=self.profile,
            title='Test Review',
            content='This is a test review.',
            rating=5
        )

    def test_review_str(self):
        self.assertEqual(
            str(self.review),
            f'{self.profile.user.username} → {self.book.title}'
        )

    def test_unique_review_per_user_per_book(self):
        with self.assertRaises(Exception):
            Review.objects.create(
                book=self.book,
                author=self.profile,
                title='Another Review',
                content='Duplicate review',
                rating=4
            )



class ReviewTagModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.profile = Profile.objects.create(user=self.user)

        self.book = Book.objects.create(
            title='Test Book',
            author='Test Author'
        )

        self.review = Review.objects.create(
            book=self.book,
            author=self.profile,
            title='Test Review',
            content='Test content',
            rating=4
        )

        self.tag = Tag.objects.create(name='Test Tag')

        self.review_tag = ReviewTag.objects.create(
            review=self.review,
            tag=self.tag
        )

    def test_review_tag_str(self):
        self.assertEqual(
            str(self.review_tag),
            f'{self.review} #{self.tag.name}'
        )

    def test_unique_together(self):
        with self.assertRaises(Exception):
            ReviewTag.objects.create(
                review=self.review,
                tag=self.tag
            )
