import datetime
from form import logInForm, ContactForm, SettingForm, SignUpForm
from flask import Flask, render_template, request, flash, redirect, url_for, make_response
from flaskSQLAuthorised import ValidateNewUserLogIn, InvalidCredential, Authenticated, AuthenticatedRenderTemplate, SecureString, SQLExecute
import mysql.connector


app = Flask(__name__)
app.config['SECRET_KEY'] = '123456' #this helps to stop attacks on the website when submitting info
array = [0,1,2,3,4,5]


#this is the first page they will see, it has two ways of accessing it '/' and '/login'
@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
#the get and post methods refer to whether the infomation is being sent or received

def LoginPage():
    Error = ''
    form = logInForm
    try:
        if request.method == "POST":                                                               #if the method is post (e.g. if the user has submited the form
            print(request.form['username'])
            Username = ValidateNewUserLogIn(request.form['username'], request.form['password'])
            if Username[0] != "#":                                                               #if the user is unknown the AutheicatedUser returns #
                print(Username + ' Logged on at ' + datetime.datetime.now().strftime("%c"))
                return AuthenticatedRenderTemplate("calendar_page.html", Username)

            else:                                                                                  #this would be used if the AuthenticatedUser couldn't find the user
                Error = "Invalid credentials. Try Again: " + Username                              #this tells the user the error

        return render_template("login_page.html", Error=Error, form=form)                          #return the template, this is the page with the form on it

    except Exception as e:
        Error = 'Code Issue'
        return render_template("login_page.html", Error=Error, form=form)




'''
#this function allows me to enter in any SQL statement and removes the need to repeatedly connect and retype.
#The SQL command is the acutal command, the SQLAddress is any variables and the type if whether i want results returned or just a command executed
def SQLExecute(SQLCommand, SQLAddress,type):
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="PenygelliSQL2!",
    )

    # TheCursor is linked to the Database
    TheCursor = db.cursor()
    TheCursor.execute(SQLCommand, SQLAddress)
    if type == 'r':
        Results = TheCursor.fetchall()
        return Results
    db.commit()
    db.close()
'''

@app.route('/signup',methods=['GET','POST'])
def signup():
    form = SignUpForm()
    if request.method == 'POST':
        if not form.validate():
            ErrorEmpty = 'All fields are required'
            return render_template('signup_page.html', form=form, ErrorEmpty=ErrorEmpty)

        SQLExecute('''INSERT INTO NEADatabase2.tblusers (UserName,Password,SecurityAnswer,FirstName,Surname,KnownAsName,tblsecurity_QuestionId,tbltitle_TitleId)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s)''',(request.form['username'],request.form['password'],request.form['securitya'],
                                                        request.form['firstname'],request.form['surname'],request.form['knownas'],
                                                        request.form['securityq'],request.form['title']),'e')
        return redirect(url_for('LoginPage'))
        #form = logInForm
        #return render_template('login_page.html', form=form)


    if request.method == 'GET':
        titles = []
        questions = []
        results = SQLExecute('''SELECT * FROM NEADatabase2.tbltitle''',(),'r')
        for r in results:
            titles.append('<option value="'+str(r[0]) + '">' + str(r[1]) + '</option>')

        results = SQLExecute('''SELECT * FROM NEADatabase2.tblsecurity''', (), 'r')
        for r in results:
            questions.append('<option value="'+str(r[0])+'">'+str(r[1])+'</option>')

        return render_template('signup_page.html',form=form, titles=titles, questions=questions)



#app routes are the main pages of the website, you can add as many names to each route


#tempory page
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()

    if request.method == 'POST':
        print(request.form["Age"])
        if not form.validate():
            flash('All fields are required.')
            return render_template('contact.html', form=form)
        else:
            #return display()
            return render_template('display_page.html', title=request.form['Age'], form=form)

    if request.method == 'GET':
        return render_template('contact.html', form=form)


@app.route('/notes')
def notes():
    Username = request.cookies.get('User')
    print('User: ' + Username + ' requests page tasks')
    if InvalidCredential(Username, request.cookies.get('ID')):
        # User Timed out / Logged Out / or unauthorised request
        return render_template('login_page.html')  # this renders the login page template
    # Continue with Page preparation as user is Valid

    return AuthenticatedRenderTemplate('notes_page.html', Username)  # this renders the display tasks template and resets session / cookie


@app.route('/settings', methods=['GET','POST'])
def settings():
    form = SettingForm()

    if request.method == 'POST':
        print("sent")
        NewFirstname = request.form["fname"]
        NewSecond = request.form["sname"]
        NewTitle = request.form["title"]
        NewKnownas = request.form["knownas"]

        print(NewFirstname,NewSecond,NewTitle,NewKnownas)

        #updates the SQL database with the new data the user has entered
        SQLExecute("""UPDATE NEADatabase2.tblusers SET tblusers.FirstName = %s, tblusers.Surname = %s, tblusers.Title = %s, tblusers.KnownAsName = %s 
                    WHERE tblusers.Username = %s""",(NewFirstname,NewSecond,NewTitle,NewKnownas,'rhianmack'),'e')

        return render_template('settings_page.html', form=form)


    if request.method == 'GET':

        Results = SQLExecute("""SELECT * FROM NEADatabase2.tblusers WHERE tblusers.username = %s""",("rhianmack",),'r')
        for x in Results:
            firstname = x[5]
            surname = x[6]
            knownas = x[8]
            title = x[7]
        return render_template('settings_page.html', form=form, EFirstname = firstname, ESurname = surname, Eknownas = knownas, Etitle = title)



@app.route('/stats')
def stats():
    return render_template('stats_page.html')

@app.route('/calendar',methods=['GET','POST'])
def calendar():
    Username = request.cookies.get('User')
    print('User: ' + Username + ' requests page calendar')
    if InvalidCredential(Username, request.cookies.get('ID')):
        # User Timed out / Logged Out / or unauthorised request
        return render_template('login_page.html')  # this renders the login page template
    # Continue with Page preparation as user is Valid

    return AuthenticatedRenderTemplate('calendar_page.html', Username)  # this renders the display tasks template and resets session / cookie


@app.route('/display')
def display():
    lists = []
    result = SQLExecute('''SELECT * FROM NEADatabase2.tblusers''',())
    for row in result:
        FullName = row[7]+" "+row[5]+" "+row[6]
        username = row[1]
        password = row[2]

        lists.append({FullName,username,password})

    print(lists)
    return render_template('display_page.html', title='a', posts=lists)  # this renders the display page template but poor control

    cursor.close

@app.route('/logout')
def logout():

    Username  = request.cookies.get('User')
    print('User: ' + Username + ' Logging Out')
    if InvalidCredential(Username, request.cookies.get('ID')):
        # User Timed out / Logged Out / or unauthorised request
        return render_template('login_page.html')  # this renders the login page template
    # Continue with Page preparation as user is Valid
    SQLExecute("UPDATE tblusers SET SessionID = %s, SessionExpire = %s Where UserName = %s",
              ("Logged Out - "+SecureString(8,65,91), datetime.datetime.now(), Username))
    res = make_response(render_template('logout_page.html',title=Username))
    res.set_cookie('ID', 'w', max_age=0)
    res.set_cookie('User', 'loggedout', max_age=0)
    return res  # this renders login page template

@app.route('/account')
def account():
    Username  = request.cookies.get('User')
    print('User: ' + Username + ' requests page calendar')
    if InvalidCredential(Username, request.cookies.get('ID')):
        # User Timed out / Logged Out / or unauthorised request
        return render_template('login_page.html')  # this renders the login page template
    # Continue with Page preparation as user is Valid

    LastComp = ''
    ThisRow = [
        [
            'Company Name',
            'Address'
        ]
    ]
    ThisList= [ThisRow]

    result = SQLExecute("""SELECT CompanyUsersID, testdatabase.tblcompany.companyname,  testdatabase.tblcompany.companyaddress, testdatabase.tblusers.UserName FROM testdatabase.tblcompanyusers 
    INNER JOIN testdatabase.tblcompany ON testdatabase.tblcompany.companyid = testdatabase.tblcompanyusers.Company 
    INNER JOIN testdatabase.tblusers ON testdatabase.tblusers.UserID = testdatabase.tblcompanyusers.Users Where UserName = %s; """, (Username, ))
    print(result)

    for row in result:
        #print(row[1])
        LastComp = format(LastComp) + row[1] + '-'
        ThisRow = [
            [
                row[1],
                row[2]
            ]
        ]
        ThisList.append(ThisRow)
        #print(ThisRow)
    #return render_template('testdisplay_page.html', title="Test Display Page - " + SecureString(4,65,91), posts = ThisList)  # this renders the display page template
    # Generate SessionTokenCode
    SessionTokenCode = SecureString(8, 65, 91)
    # Modify SQL Database with Session and Expiry Date/Time
    SQLExecute("UPDATE tblusers SET SessionID = %s, SessionExpire = %s Where UserName = %s",
              (SessionTokenCode, datetime.datetime.now() + datetime.timedelta(0, 60 * 10), Username))
    # Set up Webpage to reply to User with including Cookies for future authenticated use
    res = make_response(render_template('display_account.html', title=Username, posts = ThisList))
    res.set_cookie('ID', SessionTokenCode, max_age=60 * 10)
    res.set_cookie('User', Username, max_age=60 * 10)
    return res


@app.route('/test')
def test():
    LastComp = ''
    ThisRow = [
        [
            'Company Name',
            'User Name'
        ]
    ]
    ThisList= [ThisRow]

    #result = SQLExecute("""Select Password, SessionID, UserName FROM testdatabase.tblusers ""","")
    result = SQLExecute("""SELECT CompanyUsersID, testdatabase.tblcompany.companyname, testdatabase.tblusers.UserName FROM testdatabase.tblcompanyusers 
    INNER JOIN testdatabase.tblcompany ON testdatabase.tblcompany.companyid = testdatabase.tblcompanyusers.Company 
    INNER JOIN testdatabase.tblusers ON testdatabase.tblusers.UserID = testdatabase.tblcompanyusers.Users; """, "")
    print(result)

    for row in result:
        #print(row[1])
        LastComp = format(LastComp) + row[1] + '-'
        ThisRow = [
            [
                row[1],
                row[2]
            ]
        ]
        ThisList.append(ThisRow)
        #print(ThisRow)
    return render_template('testdisplay_page.html', title="Test Display Page - " + SecureString(4,65,91), posts = ThisList)  # this renders the display page template


#this means it only runs if i am running it directly from this script
if __name__ == '__main__':
    app.run()
    # Next line to share on a local network
    # app.run(host= '0.0.0.0')
    # Failed code to run on default html port!
    #    app.run(host = '0.0.0.0', port=80)
    # Code to change debug mode.
    app.debug = True