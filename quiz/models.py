from django.db import models


def all_as_dto():
    quizzes = Quiz.objects.order_by('uuid')

    # TODO: implement Model to DTO
    quizzes_dto = []
    return quizzes_dto


class Quiz(models.Model):
    uuid = models.UUIDField()
    title = models.CharField(max_length=100)


class Question(models.Model):
    uuid = models.UUIDField()
    text = models.CharField(max_length=200)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)


class Choice(models.Model):
    uuid = models.UUIDField()
    text = models.CharField(max_length=200)
    is_correct = models.BooleanField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
