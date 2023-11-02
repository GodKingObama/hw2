import os
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "your_secret_key"

UPLOAD_FOLDER = 'templates'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def index():
    if len(session) == 0:
        return render_template("login.html")
    else:
        return redirect(url_for("homepage"))

@app.route("/homepage_action",methods = ["POST","GET"])
def homepage_action():
    if request.method == "POST":
        inputtext = request.form["inputtext"]
        blogfile = open("blog.txt", "a") #opens blog.txt in append mode. Creates blogfile object
        blogfile.write(inputtext+"\n") #writes input text into blogfile, then creates new line. 
        blogfile.close()
        return homepage()

@app.route("/homepage")
def homepage():
    webpage = '''
    <html>
    <head>
    <title>Home</title>
    </head>
    <body>
    <p style='text-align:left;'>
    <h1>Welcome to the TECH 136 blog by LAM
    <span style='float:right;'>
    Username:
    ''' + session["username"] + " <a href='" + url_for("logout") + "'>Logout</a></h1></span></p>"

    webpage += '''
    <form action = 'homepage_action' method = 'post'>
    Enter your comment here:
    <br>
    <textarea id='inputtext' name='inputtext' rows='2' cols='100'></textarea>
    <br>
    <input type = 'submit' value = 'Submit' />
    <a href="/upload">OR Upload image</a>
    <br>
    <br>
    '''   

    with open("blog.txt", "r") as blogfile: #opens blog,txt in read mode, creates object blogfile.
            blog = blogfile.read().rstrip() #blog is the read file. Strips the right side of the blog file (removes spaces at end)
    blogfile.close()
    bloglist = blog.split("\n") #bloglist is a variable that takes blog, splits it at each \n (line break).

    for i in range(len(bloglist)): # creates a for loop with the legnth of the elements in bloglist. If there are 3 posts, it'll do it 3 times.
            webpage += bloglist[i]+"<br>\n" #indexes bloglist one at a time and adds html break

    return webpage

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        
        blogfile = open("blog.txt", "a") #opens blog.txt in append mode. Creates blogfile object
        print("upload file")
        blogfile.write("<img src=\"" + file.filename+ "\">"+"\n") 
        blogfile.close()
        return homepage()

    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

@app.route("/login_action",methods = ["POST","GET"])
def login_action():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        # Dummy user validation
        if username == "guest" and password == "password":
            session["username"] = username
            return redirect(url_for("homepage"))

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("username", None)
    return render_template("login.html")

# main driver function
if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5009)
