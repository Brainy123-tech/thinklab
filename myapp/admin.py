from django.contrib import admin
from .models import About
from .models import Testimonial
from .models import BlogPost
from .models import Subject, Quiz, Question, Answer

 #Register your models here.
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'slide', 'video')
    search_fields = ('title', 'description')

class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    fields = ('title', 'content', 'image', 'video_url', 'external_link')  # 👈 Include this


admin.site.register(About)

admin.site.register(Testimonial)


admin.site.register(BlogPost, BlogPostAdmin)

admin.site.register(Subject)
admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question)
admin.site.register(Answer)
