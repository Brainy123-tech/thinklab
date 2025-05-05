from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from myapp.utils import run_simulation
from .models import About, Testimonial, BlogPost, UserProfile, Subject, Quiz, Answer, UserAnswer
#from django.http import HttpResponse
from django.contrib.auth import logout
from django.http import HttpResponseBadRequest
from .forms import ProfilePictureForm
from .forms import SimulationForm
import random
from .models import Comment  

def index(request):
    about = About.objects.first()  # or .last(), or get(id=1), depending on your logic
    #return render(request, 'your_template.html', )
    return render(request, 'index.html',{'about': about})

def blog_post_list(request):
    posts = BlogPost.objects.all()  # Assuming you have a BlogPost model
    return render(request, 'blog_post_list.html', {'posts': posts})


# Signup view
def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')


        # Validate the data
        if not username or not email or not password or not confirm_password:
            messages.error(request, "All fields are required.")
        elif password != confirm_password:
            messages.error(request, "Passwords do not match.")
        elif len(password) < 6:
            messages.error(request, "Password must be at least 6 characters.")
        else:
            try:
                user = User.objects.create_user(username=username, email=email, password=password)
                messages.success(request, "Account created successfully! You can now log in.")
                return redirect('login')
            except Exception as e:
                messages.error(request, f"Error: {str(e)}")
    
    return render(request, 'signup.html')

# Login view
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have successfully logged in!")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'login.html')

# Dashboard view
#@login_required
@login_required
def dashboard(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    # Redirect if user hasn't paid
    #if not profile.has_paid:
        #return redirect('payment_page')

    if request.method == 'POST':
        if 'profile_picture' in request.FILES:
            # Handle profile picture upload
            form = ProfilePictureForm(request.POST, request.FILES, instance=profile)
            if form.is_valid():
                form.save()
                messages.success(request, 'Profile picture updated successfully!')
                return redirect('dashboard')
        else:
            # Handle new comment
            comment_text = request.POST.get('comment')
            if comment_text:
                Comment.objects.create(user=request.user, text=comment_text)
                messages.success(request, 'Comment posted successfully! 🎉')
                return redirect('dashboard')

    else:
        form = ProfilePictureForm(instance=profile)

    about = About.objects.first()
    testimonials = Testimonial.objects.all()
    comments = Comment.objects.all().order_by('-created_at')  # Fetch comments

    return render(request, 'dashboard.html', {
        'user': request.user,
        'about': about,
        'testimonials': testimonials,
        'comments': comments,
        'form': form,
        'profile': profile
    })

# Logout view
def logout_view(request):
    logout(request)
    return redirect('index')

# Payment page
def payment_page(request):
    if request.method == 'POST':
        # Simulate payment process
        profile = request.user.userprofile
        profile.has_paid = True
        profile.save()

        # Retrieve the quiz ID from session (if any)
        quiz_id = request.session.get('quiz_to_take')
        if quiz_id:
            # Remove it from session after using
            del request.session['quiz_to_take']
            return redirect('take_quiz', quiz_id=quiz_id)
        
        # Default redirect if no quiz_id was stored
        return redirect('take_quiz')  # or any fallback view
    
    return render(request, 'payment_page.html')

# Quiz page view
def quiz_page(request):
    subjects = Subject.objects.prefetch_related('quiz_set').all()
    quizzes = Quiz.objects.all()
    return render(request, 'quiz_page.html', {
        'subjects': subjects,
        'quizzes': quizzes
    })
# Take quiz view
def take_quiz(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    context = {'quiz': quiz}
    return render(request, 'take_quiz.html', context)

# Submit quiz view
def submit_quiz(request, quiz_id):
    if request.method != 'POST':
        return HttpResponseBadRequest("Invalid request method")

    quiz = get_object_or_404(Quiz, id=quiz_id)
    user = request.user

    for question in quiz.questions.all():
        field_name = f'question_{question.id}'
        submitted_value = request.POST.get(field_name)

        if submitted_value:
            if question.question_type == "MCQ":
                try:
                    selected_answer = Answer.objects.get(id=submitted_value)
                    is_correct = selected_answer.correct
                    UserAnswer.objects.create(
                        user=user,
                        question=question,
                        selected_answer=selected_answer,
                        is_correct=is_correct
                    )
                except (Answer.DoesNotExist, ValueError):
                    # Invalid ID submitted
                    UserAnswer.objects.create(
                        user=user,
                        question=question,
                        selected_answer=None,
                        is_correct=False
                    )
            elif question.question_type == "SHORT":
                # Save the typed short answer
                UserAnswer.objects.create(
                    user=user,
                    question=question,
                    short_answer=submitted_value,
                    selected_answer=None,
                    is_correct=False  # You can add logic later to check correctness
                )
        else:
            # No answer submitted
            UserAnswer.objects.create(
                user=user,
                question=question,
                selected_answer=None,
                is_correct=False
            )

    return redirect('quiz_result', quiz_id=quiz.id)

    

# View answers after quiz
def view_answers(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    user_answers = UserAnswer.objects.filter(user=request.user, question__quiz=quiz)
    return render(request, 'quiz/view_answers.html', {'quiz': quiz, 'user_answers': user_answers})

# Quiz result view
def quiz_result(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    
    user_answers = UserAnswer.objects.filter(
        user=request.user,
        question__quiz=quiz
    ).select_related('question', 'selected_answer')

    score = sum(1 for answer in user_answers if answer.is_correct)
    total_questions = quiz.questions.count()

    # Calculate if the user passed (score >= half of total questions)
    passed = score >= total_questions / 2

    # Optionally, calculate the score percentage
    score_percentage = (score / total_questions) * 100

    context = {
        'quiz': quiz,
        'score': score,
        'total_questions': total_questions,
        'user_answers': user_answers,
        'passed': passed,
        'score_percentage': score_percentage,  # Pass the score percentage
    }
    return render(request, 'quiz_result.html', context)



def submit_answers(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)  # Get the quiz based on the quiz_id
    
    if request.method == 'POST':
        # Process submitted answers here
        answers = request.POST.getlist('answers')  # Assuming answers are posted as a list
        # Save or process the answers accordingly
        for answer in answers:
            # Create or update Answer model here
            Answer.objects.create(quiz=quiz, answer_text=answer)
            
        # You can redirect to a confirmation page or show a success message
        return render(request, 'quiz/thank_you.html', {'quiz': quiz})
    
    return render(request, 'quiz/quiz_detail.html', {'quiz': quiz})

def project_list(request):
    return render(request, 'project_list.html')

def animal_ecology_view(request):
    return render(request, 'animal_ecology.html')

def simulation(request):
    return render(request, 'simulation.html')

#def simulation(request):
    if request.method == 'POST':
        form = SimulationForm(request.POST)
        if form.is_valid():
            animal_type = form.cleaned_data['animal_type']
            simulation_speed = form.cleaned_data['simulation_speed']

            # 🚀 Add simulation logic here
            result_data = run_simulation(animal_type, simulation_speed)

            context = {
                'animal_type': animal_type,
                'simulation_speed': simulation_speed,
                'simulation_summary': result_data['summary'],
                'success_rate': result_data['success_rate'],
                'recommendations': result_data['recommendations'],
            }
            return render(request, 'simulation_result.html', context)
    else:
        form = SimulationForm()

    return render(request, 'simulation.html', {'form': form})
def simulation(request):
    # You can replace this logic with real simulation later
    animal_types = ['K-strategist', 'r-strategist']
    animal_type = random.choice(animal_types)

    final_population = random.randint(20, 100)  # Just an example
    predation = random.randint(10, 50)
    food = random.randint(50, 100)
    reproduction = random.randint(30, 70)

    context = {
        'animal_type': animal_type,
        'final_population': final_population,
        'predation': predation,
        'food': food,
        'reproduction': reproduction,
    }

    return render(request, 'simulation.html', context)

def simulation_result(request):
    # This view will render the simulation result page
    # If you pass data to it, you can access it in the template
    return render(request, 'simulation_result.html')

