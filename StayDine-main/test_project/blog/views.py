from django.shortcuts import render

# Create your views here.
# posts = [
#     {
#         'author': 'CoreyMS',
#         'title': 'Blog Post 1',
#         'content': 'First post content',
#         'date_posted': 'August 27, 2018'
#     },
#     {
#         'author': 'Jane Doe',
#         'title': 'Blog Post 2',
#         'content': 'Second post content',
#         'date_posted': 'August 28, 2018'
#     }
# ]

def home(req):
    # context = {
    #     'posts': posts
    # }
    return render(req, 'blog/home.html')


def about(req):
    return render(req, 'blog/about.html', {'title': 'About'})

def bookings(req):
    return render(req, 'blog/bookings.html', {'title': 'Bookings'})

def menu(req):
    return render(req, 'blog/menu.html', {'title': 'Menu'})

def events(req):
    return render(req, 'blog/events.html', {'title': 'Events'})

def tables(req):
    return render(req, 'blog/tables.html', {'title': 'Table Reservation'})
