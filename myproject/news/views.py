from django.shortcuts import render
from .models import Author, Category, Post, Comment

def index(request):
    user1 = User.objects.create_user('user1')
    user2 = User.objects.create_user('user2')


    author1 = Author.objects.create(user=user1)
    author2 = Author.objects.create(user=user2)


    category1 = Category.objects.create(name='Спорт')
    category2 = Category.objects.create(name='Политика')
    category3 = Category.objects.create(name='Образование')
    category4 = Category.objects.create(name='Наука')


    post1 = Post.objects.create(author=author1, type='article', title='Статья 1', content='Содержимое статьи 1')
    post2 = Post.objects.create(author=author2, type='article', title='Статья 2', content='Содержимое статьи 2')
    post3 = Post.objects.create(author=author1, type='news', title='Новость 1', content='Содержимое новости 1')


    post1.categories.add(category1, category2)
    post2.categories.add(category3)
    post3.categories.add(category4)


    comment1 = Comment.objects.create(post=post1, user=user1, text='Комментарий 1')
    comment2 = Comment.objects.create(post=post2, user=user2, text='Комментарий 2')
    comment3 = Comment.objects.create(post=post3, user=user1, text='Комментарий 3')
    comment4 = Comment.objects.create(post=post1, user=user2, text='Комментарий 4')


    post1.like()
    post1.dislike()
    post2.like()
    comment1.like()
    comment2.dislike()
    comment3.like()
    comment4.dislike()


    author1.update_rating()
    author2.update_rating()


    best_author = Author.objects.order_by('-rating').first()
    best_user = best_author.user
    print(f"Лучший пользователь: {best_user.username}, рейтинг: {best_author.rating}")


    best_post = Post.objects.filter(type='article').order_by('-rating').first()
    print(f"Лучшая статья:\n"
          f"Дата добавления: {best_post.created_at}\n"
          f"Автор: {best_post.author}\n"
          f"Рейтинг: {best_post.rating}\n"
          f"Заголовок: {best_post.title}\n"
          f"Превью: {best_post.preview()}")


    comments = Comment.objects.filter(post=best_post)
    for comment in comments:
        print(f"Дата: {comment.created_at}\n"
              f"Пользователь: {comment.user.username}\n"
              f"Рейтинг: {comment.rating}\n"
              f"Текст: {comment.text}")

    return render(request, 'index.html')