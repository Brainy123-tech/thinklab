from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User



# Create your models here.
class About(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.TextField()
    paragraph_one = models.TextField()
    bullet_1 = models.CharField(max_length=255)
    bullet_2 = models.CharField(max_length=255)
    bullet_3 = models.CharField(max_length=255)
    paragraph_two = models.TextField()
    read_more_link = models.URLField(blank=True)
    image = models.ImageField(upload_to='about_images/', null=True, blank=True)


    def __str__(self):
        return self.title
    

class Testimonial(models.Model):
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    text = models.TextField()
    image = models.ImageField(upload_to='testimonials/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.role}"
    

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)
    external_link = models.URLField(blank=True, null=True)
  

    def __str__(self):
        return self.title



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    has_paid = models.BooleanField(default=False)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return self.user.username
    

class Subject(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Quiz(models.Model):
    title = models.CharField(max_length=255)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    slide = models.FileField(upload_to='slides/', blank=True, null=True)
    video = models.FileField(upload_to='videos/', blank=True, null=True)
    description = models.TextField()


    def __str__(self):
        return self.title

class Question(models.Model):
    QUESTION_TYPES = (
        ('MCQ', 'Multiple Choice'),
        ('SHORT', 'Short Answer'),
    )

    quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE)
    text = models.TextField()
    question_type = models.CharField(max_length=10, choices=QUESTION_TYPES, default='MCQ')
    correct_text_answer = models.CharField(max_length=255, blank=True, null=True)  # only used for SHORT

    def __str__(self):
        return self.text


class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text
    



class UserAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    selected_answer = models.ForeignKey('Answer', null=True, blank=True, on_delete=models.SET_NULL)
    is_correct = models.BooleanField(default=False)
    short_answer = models.TextField(null=True, blank=True)  # <-- Add this line

    def __str__(self):
        return f"{self.user.username} - {self.question.text}"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.text[:20]}'
