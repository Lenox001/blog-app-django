from django.shortcuts import render, redirect
from django import forms
from django.http import HttpResponse
from .models import Contact
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import UserRegisterForm, UserLoginForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Sample blog posts data
blog_posts = [
    {
        "title": "Understanding Artificial Intelligence",
        "author": "Jane Doe",
        "date": "September 25, 2024",
        "link": "https://www.ibm.com/cloud/learn/what-is-artificial-intelligence",
        "description": "Explore the fundamentals of artificial intelligence and its impact on various industries.",
        "image": "images/AI.png"
    },
    {
        "title": "The Future of Renewable Energy",
        "author": "John Smith",
        "date": "September 22, 2024",
        "link": "https://www.energy.gov/eere/solar/articles/future-solar-energy",
        "description": "An in-depth look at the latest advancements in renewable energy technologies and their potential.",
        "image": "images/renewable.jpeg"
    },
    {
        "title": "Top 10 Programming Languages in 2024",
        "author": "Emily Johnson",
        "date": "September 20, 2024",
        "link": "https://www.codecademy.com/resources/blog/best-programming-languages-to-learn/",
        "description": "Discover the most popular programming languages to learn this year and their applications.",
        "image": "images/programming.png"
    },
    {
        "title": "A Guide to Mindfulness Meditation",
        "author": "Michael Brown",
        "date": "September 15, 2024",
        "link": "https://www.mindful.org/meditation/mindfulness-getting-started/",
        "description": "Learn about the benefits of mindfulness meditation and practical tips to get started.",
        "image": "images/meditation.png"
    },
    {
        "title": "Exploring the Great Outdoors: Hiking Tips",
        "author": "Sarah Wilson",
        "date": "September 10, 2024",
        "link": "https://www.rei.com/learn/expert-advice/hiking-tips.html",
        "description": "Essential tips and tricks for hiking to ensure a safe and enjoyable experience.",
        "image": "images/hiking.png"
    },
    {
        "title": "The Impact of Social Media on Society",
        "author": "David Lee",
        "date": "September 8, 2024",
        "link": "https://www.pewresearch.org/internet/2020/06/12/the-state-of-social-media/",
        "description": "An analysis of how social media influences our lives and the world around us.",
        "image": "images/socials.png"
    },
    {
        "title": "Cooking 101: Easy Recipes for Beginners",
        "author": "Jessica Taylor",
        "date": "September 5, 2024",
        "link": "https://www.bbcgoodfood.com/recipes/collection/easy-recipes",
        "description": "Simple and delicious recipes for those new to cooking, perfect for honing your skills.",
        "image": "images/recipe.jpg"
    },
    {
        "title": "The Rise of E-commerce",
        "author": "Brian Miller",
        "date": "September 3, 2024",
        "link": "https://www.shopify.com/blog/ecommerce-trends",
        "description": "A look at the growth of e-commerce and trends shaping the future of online shopping.",
        "image": "images/ecomm.png"
    },
    {
        "title": "Fitness Tips for a Healthy Lifestyle",
        "author": "Anna Garcia",
        "date": "September 1, 2024",
        "link": "https://www.healthline.com/nutrition/fitness-tips",
        "description": "Expert advice on how to maintain a healthy lifestyle through fitness and nutrition.",
        "image": "images/fitness.png"
    },
    {
        "title": "Traveling on a Budget: Tips and Tricks",
        "author": "Kevin Martinez",
        "date": "August 30, 2024",
        "link": "https://www.nomadicmatt.com/travel-blogs/budget-travel-tips/",
        "description": "Proven strategies for traveling on a budget without sacrificing experience.",
        "image": "images/travel.jpeg"
    }
]

@login_required
def index(request):
    return render(request, 'blog/index.html', {
        "blog_posts": blog_posts,
        "username": request.user.username
    })

@login_required
def about(request):
    return render(request, 'blog/about.html')

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)

@login_required
def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Save the contact data to the database
            contact = Contact(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                message=form.cleaned_data['message']
            )
            contact.save()
            return redirect('success')  # Redirect to a success page
    else:
        form = ContactForm()

    return render(request, 'blog/contact.html', {'form': form})

def success_view(request):
    return HttpResponse("Thank you for your message! We'll get back to you soon.")

@login_required
def services(request):
    return render(request, 'blog/services.html')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            
            # Check if the username already exists
            if User.objects.filter(username=username).exists():
                messages.error(request, f'Username "{username}" already exists. Please choose a different one.')
            else:
                # Save the user if the username is unique
                form.save()
                messages.success(request, f'Account created for {username}!')
                return redirect('login')  # Redirect to login after registration
    else:
        form = UserRegisterForm()

    return render(request, 'blog/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')  # Redirect to the homepage after login
            else:
                messages.error(request, 'Invalid username or password')
        form = UserLoginForm()  # Recreate the form to avoid form re-submission
    else:
        form = UserLoginForm()
    return render(request, 'blog/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to login after logout
