from flask import Flask, render_template
from form import logInForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '123456' #this helps to stop attacks on the website when submitting info
array = [0,1,2,3,4,5]

#app routes are the main pages of the website, you can add as many names to each route
'''  #
@app.route('/home')
def home():
    return render_template('home_page.html')''' #this renders the home page template

#this is the first page they will see
@app.route('/')
@app.route('/login')
def login():
    form = logInForm()
    return render_template('login.html', title='Log in', form=form)


#this means it only runs if i am running it directly from this script
if __name__ == '__main__':
    app.run()