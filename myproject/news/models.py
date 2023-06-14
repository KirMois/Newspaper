from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)  # Добавлена поле рейтинг

    def update_rating(self):
        pass


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    CHOICES = (
        ('article', 'Статья'),
        ('news', 'Новость'),
    )
    type = models.CharField(max_length=7, choices=CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=255)
    content = models.TextField()
    rating = models.IntegerField(default=0)  # Добавлена поле рейтинг

    def preview(self):
        return self.content[:124] + '...' if len(self.content) > 124 else self.content


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)  # Добавлена поле рейтинг

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)  # Добавлена поле рейтинг

    def update_rating(self):
        post_rating = self.post_set.aggregate(models.Sum('rating'))['rating__sum'] or 0
        comment_rating = self.user.comment_set.aggregate(models.Sum('rating'))['rating__sum'] or 0
        comment_rating_to_posts = self.post_set.annotate(comment_rating=models.Sum('comment__rating')).aggregate(models.Sum('comment_rating'))['comment_rating__sum'] or 0

        self.rating = post_rating * 3 + comment_rating + comment_rating_to_posts
        self.save()