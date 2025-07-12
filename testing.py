from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def home():
    return "This is the home page"

@app.get('/about')
def about():
    return 'This is a testing code for fastapi'