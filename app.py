from flask import Flask, Response, redirect, render_template, request
import requests
import requests_cache
from github import prepare_user_info
from graphs import graph_types

requests_cache.install_cache('github_cache', expire_after=86400)
import base64
app = Flask(__name__, static_url_path='/static')

@app.route('/')
def hello():
    return render_template("index.html")

@app.route('/summary')
def get_summary():
    username = request.args.get('username')
    if username is None:
        return redirect('/')
    
    user_info_endpoint = "https://api.github.com/users/" + username
    request_made = requests.get(user_info_endpoint)
    if request_made.status_code == 403:
        status = request_made.json()
        return render_template("summary.html", data=None, status=status, username=username)
    if not request_made.ok:
        return render_template('no_user.html', username=username)
    
    template_data = prepare_user_info(username, request_made.json())
    return render_template("summary.html", data=template_data, status=None, username=username)

@app.route('/graph')
def get_individual_graph():
    graph_type = request.args.get('graph_type')
    username = request.args.get('username')    
    user_info_endpoint = "https://api.github.com/users/" + username

    if username is None or graph_type.lower()  not in graph_types:
        return "Error: Missing or invalid parameters (username and graph_type are required).", 400
    try:

        request_made = requests.get(user_info_endpoint)
        request_made.raise_for_status()
        user_info_request_content = request_made.json()
        all_data = prepare_user_info(username, user_info_request_content)
        graph =  all_data[graph_type.lower()]
        if not graph:
            return 'No graph available at this time'
        data_url = graph.get('img')
        if data_url.startswith("data:image/png;base64,"):
            base64_data = data_url.split(",", 1)[1]
            binary_data = base64.b64decode(base64_data)
        else:
            binary_data = data_url

        return Response(binary_data, mimetype='image/png')
    except (requests.RequestException, ValueError):
            return 'Error Server Fault'
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)