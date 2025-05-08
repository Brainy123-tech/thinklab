from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('blog/', views.blog_post_list, name='blog_post_list'),
    #path('payment/', views.payment_page, name='payment_page'),
    #path('payment/<int:quiz_id>/', views.payment_page, name='payment_page'),
    path('quiz/', views.quiz_page, name='quiz_page'),
    path('quiz/<int:quiz_id>/', views.take_quiz, name='take_quiz'),
    path('quiz/<int:quiz_id>/submit/', views.submit_quiz, name='submit_quiz'),
    #path('quiz/<int:quiz_id>/answers/', views.submit_answers, name='submit_answers'),
    path('quiz/<int:quiz_id>/answers/', views.view_answers, name='view_answers'),
    #path('quiz/<int:quiz_id>/submit/', views.submit_quiz, name='submit_quiz'),
    path('quiz/<int:quiz_id>/result/', views.quiz_result, name='quiz_result'),
    path('projects/', views.project_list, name='project_list'),
    path('animal-ecology/', views.animal_ecology_view, name='animal_ecology'),
    path('simulation/', views.simulation, name='simulation'),
    path('simulation-result/', views.simulation_result, name='simulation_result'),


]