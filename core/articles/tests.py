from django.test import TestCase
from django.utils.translation import pgettext
from core.articles.models import Article
from core.users.models import CustomUser, SellerUser

# Create your tests here.


class ArticleModelTests(TestCase):
    def test_get_published_article(self):

        user1 = CustomUser(username='Vale', email='vale@gmail.com',
                           first_name='Valentina', last_name='Fernandez')

        user1.save()

        seller1 = SellerUser(user=user1,)

        article1 = Article(author=seller1,
                           title='Microfono FIFINE',
                           description='Microfono super mega profesional, se escucha bien chido one',
                           price=800,
                           stock=2,
                           slug='aliexpress.com/slug-001-20',
                           status='published')
        article1.save()

        article2 = Article(author=seller1,
                           title='Microfono SHURE',
                           description='Microfono super mega kk, se escucha bien chido two',
                           price=1000,
                           stock=100,
                           slug='aliexpress.com/slug-002-20',
                           status='draft')
        article2.save()

        article_test = (Article.articleobjects.all())[0]

        self.assertEqual(article_test.title, article1.title)
