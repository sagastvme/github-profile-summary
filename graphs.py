import io
import base64
import matplotlib.pyplot as plt
import requests
import matplotlib.pyplot as plt

plt.rcParams.update({
    'text.color': 'white',
    'axes.labelcolor': 'white',
    'xtick.color': 'white',
    'ytick.color': 'white',
    'axes.edgecolor': 'white',
    'figure.facecolor': '#818181',
    'axes.facecolor': 'none',      # make axes background transparent

    # Add these for bold text:
    'font.weight': 'bold',         # Makes overall font weight bold
    'axes.labelweight': 'bold',    # Makes the axes labels bold
    'axes.titleweight': 'bold',    # Makes the axes title bold
})

import matplotlib.pyplot as plt
import math  # Use math.isnan to check for NaN

def pie_chart(numbersWithLabels: dict, title: str = "My Pie Chart", graph_type=''):
    numbers = []
    labels = []
    
    for key, value in numbersWithLabels.items():
        labels.append(key)
        numbers.append(value)
    
    total = sum(numbers)

    # Handle case where all values are zero
    if total == 0:
        return False

    def make_autopct(values):
        def my_autopct(pct):
            if math.isnan(pct):  # Check if pct is NaN
                return ''  # Return empty string to avoid errors
            value = int(round(pct * total / 100.0))
            return f'{value}'
        return my_autopct
    
    # Optionally, increase the figure size to allow more space for titles/labels
    fig1, ax1 = plt.subplots(figsize=(8, 6))

    # Create the pie chart
    ax1.pie(numbers, labels=labels, autopct=make_autopct(numbers))

    # Append the total to the title
    title += f" ({total})"
    ax1.set_title(title)
    
    # Automatically adjust the layout so titles/labels are not cut off
    fig1.tight_layout()
    
    return graph_to_html_img_src(fig1, graph_type)

def graph_to_html_img_src(fig, graph_type):
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    img_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    
    # Retrieve the title from the first axes if available
    title = ""
    if fig.axes:
        title = fig.axes[0].get_title()
        
    return {'img': f"data:image/png;base64,{img_base64}", 'title': title, 'graph_type': graph_type}




def bar_chart(valueWithLabels: dict, title: str = 'My Bar Chart', ylabel='Y label', graph_type=''):
    numbers = []
    labels = []
    
    for key, value in valueWithLabels.items():
        labels.append(key)
        numbers.append(value)
    
    total = sum(numbers)
    
    # Increase figure size (optional if you need more space)
    fig, ax = plt.subplots(figsize=(8, 6))
    
    ax.bar(labels, numbers)
    
    # Update title and labels
    title += f' ({total})'
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    
    # Rotate x-axis labels if needed
    plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
    
    # Automatically adjust layout so the title/labels are not cut off
    fig.tight_layout()
    
    return graph_to_html_img_src(fig, graph_type)

graph_types = ['repos_per_language', 
               'stars_per_repo',
               'stars_per_lang', 'commits_per_repo', 'commits_per_lang',
               'commits_in_last_year']

