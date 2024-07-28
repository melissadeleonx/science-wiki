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
import datetime




# Define the index view function which renders the index page of the app
def index(request):
    # Use the list_entries() function from the given util module
    entry_titles = list_entries()

    api_key = settings.NASA_API_KEY
    api_url = f'https://api.nasa.gov/planetary/apod?api_key={api_key}'
    response = requests.get(api_url)
    data = response.json()

    context = {
        'entry_titles': entry_titles,
        'media_type': data.get('media_type'),
        'url': data.get('url'),
        'title': data.get('title'),
        'explanation': data.get('explanation')
    }

    return render(request, 'encyclopedia/index.html', context)

def all_topics(request):
     # Use the list_entries() function from the given util module
    entry_titles = list_entries()
    return render(request, 'encyclopedia/alltopics.html', {'entry_titles': entry_titles})


# Define the entry view function to render individual entry pages
def entry_page(request, title):
    entry_content = get_entry(title)
    entry_titles = list_entries()

    if not entry_content:
        error_message = "Error: 404 Not Found"
        return render(request, 'encyclopedia/error.html', {
            'error_message': error_message,
            'title': title,
            'entries': entry_titles
        }, status=404)
    else:
        html_content = markdown2.markdown(entry_content)
        og_url = request.build_absolute_uri()
        og_image = '/space.png' 

        return render(request, 'encyclopedia/entry.html', {
            'title': title,
            'content': html_content,
            'entry_titles': entry_titles,
            'og_title': title,
            'og_description': entry_content[:150], 
            'og_url': og_url,
            'og_image': og_image
        })
        

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

    try:
        response = requests.get(api_url, timeout=10)  # Set a timeout of 10 seconds
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
    except requests.exceptions.HTTPError as http_err:
        return JsonResponse({'error': f'HTTP error occurred: {http_err}'}, status=response.status_code)
    except requests.exceptions.ConnectionError:
        return JsonResponse({'error': 'Failed to connect to the API. The API might be down.'}, status=503)
    except requests.exceptions.Timeout:
        return JsonResponse({'error': 'The request to the API timed out. The API might be down.'}, status=504)
    except requests.exceptions.RequestException as err:
        return JsonResponse({'error': f'An error occurred: {err}'}, status=500)

    # If the request is successful and no exceptions are raised
    apod_data = response.json()
    return JsonResponse(apod_data)
    
    
def fetch_science_articles():
    url = 'https://en.wikipedia.org/w/api.php'
    params = {
        'action': 'query',
        'list': 'search',
        'srsearch': 'science',
        'format': 'json',
        'srlimit': 10,
        'prop': 'pageimages',
        'pithumbsize': 100
    }
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        articles = data['query']['search']
        
        for article in articles:
            page_id = article['pageid']
            page_url = f"https://en.wikipedia.org/w/api.php?action=query&prop=pageimages&format=json&pageids={page_id}&pithumbsize=100"
            page_response = requests.get(page_url)
            if page_response.status_code == 200:
                page_data = page_response.json()
                thumbnail = page_data['query']['pages'][str(page_id)].get('thumbnail', {})
                article['thumbnail'] = thumbnail.get('source', None)
        
        return articles
    return None

def featured_content_view(request):
    entry_titles = list_entries()
    articles = fetch_science_articles()
    
    if articles:
        context = {
            'articles': articles,
            'entry_titles': entry_titles
        }
        return render(request, 'encyclopedia/articles.html', context)
    else:
        error_message = 'No science-related articles found.'
        return render(request, 'encyclopedia/articles.html', {'error': error_message, 'entry_titles': entry_titles})