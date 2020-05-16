import requests
from flask import Flask, render_template, request
from scrapper import aggregate_subreddits

app = Flask("RedditNews")

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}

subreddits = [
    "javascript",
    "reactjs",
    "reactnative",
    "programming",
    "css",
    "golang",
    "flutter",
    "rust",
    "django"
]

@app.route("/")
def home():
  return render_template("home.html",subreddits = subreddits)

@app.route("/add", methods=["post"])
def add():
  new = request.form['new-subreddit']
  new_url = f"https://www.reddit.com/r/{new}"
  response = requests.get(new_url, headers = headers)
  if response.status_code == 404:
    new = "error"
    return render_template("add.html", new = new)
  elif new.startswith("/r"):
    return render_template("add.html", new = new)
  else:
    subreddits.append(new)
    return render_template("home.html",subreddits = subreddits, new = new)

@app.route("/read")
def read():
  selected = []
  for subreddit in subreddits:
    if subreddit in request.args:
      selected.append(subreddit)
  posts = aggregate_subreddits(selected)
  posts.sort(key=lambda post: post['votes'], reverse=True)
  return render_template("read.html", selected=selected, posts=posts)

app.run(host="0.0.0.0")