# views define the logic of the Wiki app

# Required modules to implement the functions
import markdown2
import random
from django.shortcuts import render, redirect
from django.urls import reverse
from .util import list_entries, get_entry, save_entry
from .forms import NewPageForm, EditEntryForm
from django.conf import settings
from django.http import JsonResponse
import requests
from .models import Article
from django.shortcuts import render, get_object_or_404



# Define the index view function which renders the index page of the app
def index(request):
    # Use the list_entries() function from the given util module
    entry_titles = list_entries()
    return render(request, 'encyclopedia/index.html', {'entry_titles': entry_titles})

def all_topics(request):
     # Use the list_entries() function from the given util module
    entry_titles = list_entries()
    return render(request, 'encyclopedia/alltopics.html', {'entry_titles': entry_titles})


# Define the entry view function to render individual entry pages
def entry_page(request, title):
    # Use the get_entry function from util module
    entry_content = get_entry(title)
    entry_titles = list_entries()


    # Check if entry content exists, render error template with 404 status if entry not found
    if not entry_content:
        error_message = "Error: 404 Not Found"
        return render(request, 'encyclopedia/error.html', {'error_message': error_message, 'title': title, 'entries': entry_content}, status=404)
    else:
        
        # Convert markdown content to HTML using the markdown2 module
        html_content = markdown2.markdown(entry_content)
        return render(request, 'encyclopedia/entry.html', {'title': title, 'content': html_content, 'entry_titles': entry_titles})
        

# To handle search request. In Django, request in views.py is always included as the first parameter of a function.
def search_wiki(request):
    # Retrieve the search query from the request GET parameters.
    query = request.GET.get('q', '').strip()
    # Get a list of all entry titles using the list_entries function from util module
    entry_titles = list_entries()

    # Make conditional statements, check for an exact match of the query in the list of entry titles
    if query:
        exact_match = None
        for entry in entry_titles:
            if entry.lower() == query.lower():
                exact_match = entry
                break
        # If there is an exact match, redirect the user to the entry page.
        if exact_match:
            return redirect('entry', title=exact_match)

        # If there is no exact match, filter the entry titles to find those containing the query as a substring.
        matching_entries = [entry for entry in entry_titles if query.lower() in entry.lower()]

                
        context = {
            'query': query,
            'entries': matching_entries,
            'entry_titles': entry_titles,
        }
        
        # Display the filtered entry titles in the search results page.
        return render(request, 'encyclopedia/search_results.html', context)
    else:
        return render(request, 'encyclopedia/search_results.html', {'entry_titles': entry_titles})
                    # If the query is not found, show a No results found message and show related topics


# Creating or adding a new entry logic
def create_page(request):
    entry_titles = list_entries()
    if request.method == 'POST':
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            if get_entry(title) is not None:
                error_message = "An entry with this title already exists."
                return render(request, 'encyclopedia/error.html', {'error_message': error_message, })
            else:
                markdown_content = f"# {title}\n\n{content}"
                save_entry(title, markdown_content)
                markdown_content = markdown2.markdown(content)
                html_content = markdown_content
                return redirect(reverse('entry', kwargs={'title': title}))
    else:
        form = NewPageForm()
    return render(request, 'encyclopedia/create.html', {'form': form, 'entry_titles': entry_titles})

def edit_page(request, title):
    # Retrieve the current content of the entry
    content = get_entry(title)
    
    if content is None:
        error_message = f"Entry '{title}' not found."
        return render(request, 'encyclopedia/error.html', {'error_message': error_message}, status=404)
    
    if request.method == 'POST':
        form = EditEntryForm(request.POST)
        
        if form.is_valid():
            updated_content = form.cleaned_data['content']
            
            updated_content_with_title = f"#{title}\n\n{updated_content}"
            
            save_entry(title, updated_content_with_title)
            
            return redirect('entry', title=title)
    else:
        content_without_title = remove_title_from_content(content)
        form = EditEntryForm(initial={'title': title, 'content': content_without_title})
    
    return render(request, 'encyclopedia/edit.html', {'title': title, 'form': form})

def remove_title_from_content(content):
    lines = content.split('\n')
    
    if lines[0].startswith('#'):
        lines = lines[1:]
    
    content_without_title = '\n'.join(lines)
    
    return content_without_title

def random_page(request):
    entries = list_entries()

    if entries:
        random_entry_title = random.choice(entries)
        return redirect('entry', title=random_entry_title)
    else:
        return render(request, 'encyclopedia/error.html', {'error_message': "No entries available."}, status=404)
    
def apod_view(request):
    api_key = settings.NASA_API_KEY
    api_url = f"https://api.nasa.gov/planetary/apod?api_key={api_key}"

    response = requests.get(api_url)
    if response.status_code == 200:
        return JsonResponse(response.json())
    else:
        return JsonResponse({'error': 'Failed to fetch data'}, status=response.status_code)

# def article_list(request):
#     articles = Article.objects.all()
#     return render(request, 'articles/articles.html', {'articles': articles})

# def feed_view(request):
#     api_key = settings.FEEDAPI_KEY 
#     url = f'https://api.feedapi.com/v1/feeds?api_key={api_key}'  # Adjust the URL based on FeedAPI documentation
#     response = requests.get(url)
    
#     if response.status_code == 200:
#         data = response.json()
#     else:
#         data = {'error': 'Unable to fetch data'}
    
#     return render(request, 'feed.html', {'data': data})