import datetime
import json
from flask import Flask,render_template,request,flash,redirect,url_for,session,logging
import wtforms
from wtforms import Form,StringField,TextAreaField,PasswordField,validators 
from passlib.hash import sha256_crypt
from functools import wraps

import requests
from flask import render_template, redirect, request

from app import app

# The node with which our application interacts, there can be multiple
# such nodes as well.
CONNECTED_NODE_ADDRESS = "http://127.0.0.1:8000"

posts = []


def fetch_posts():
    """
    Function to fetch the chain from a blockchain node, parse the
    data and store it locally need by template
    """
    get_chain_address = "{}/chain".format(CONNECTED_NODE_ADDRESS)
    response = requests.get(get_chain_address)
    if response.status_code == 200:
        content = []
        chain = json.loads(response.content)
        for block in chain["chain"]:
             content.append(block)
               

        global posts
        posts = sorted(content, key=lambda k: k['contents']['block_number'],
                       reverse=True)

#home page
@app.route('/')
def index():
    fetch_posts()
    return render_template('index.html',
                           
                           node_address=CONNECTED_NODE_ADDRESS,
                           readable_time=timestamp_to_string)


@app.route('/submit', methods=['POST'])
def submit_textarea():
    """
    Esubmit button activated to create a new transaction via our application.
    """
    post_content = request.form["content"]
    author = request.form["author"]

    post_object = {
        'author': author,
        'content': post_content,
    }

    # Submit a transaction
    new_tx_address = "{}/new_transaction".format(CONNECTED_NODE_ADDRESS)

    requests.post(new_tx_address,
                  json=post_object,
                  headers={'Content-type': 'application/json'})

    return redirect('/')


class RegisterForm(Form):
    name=StringField('Name',[validators.Length(min=1,max=50)])
    
    password=PasswordField('Password',[
            validators.DataRequired(),
                                   validators.EqualTo('confirm',message='Passwords do not match')])
    confirm=PasswordField('confirm')


@app.route('/register',methods=['GET','POST'])
def register():
    form=RegisterForm(request.form)
    print("ans for form validation is",form.validate())
    if request.method=='POST'  and form.validate():
        print("values got")
        name=form.name.data
        
        password=sha256_crypt.encrypt(str(form.password.data))
        #create cursor
        send_object={
                'name': name,
        'password': password,
                }
        new_tx_address = "{}/register_server".format(CONNECTED_NODE_ADDRESS)

        requests.post(new_tx_address,
                  json=send_object,
                  headers={'Content-type': 'application/json'})

        flash('YOUR ARE NOW REGISTERED and can login','success')
        return redirect(url_for('index'))
    return render_template('register.html',form=form)

@app.route('/results')
def result():
    get_result_address = "{}/get_result".format(CONNECTED_NODE_ADDRESS)
    response = requests.get(get_result_address)
    if response.status_code == 200:
        result = json.loads(response.content)
        # print("if succesfull let me see")
        # print(result["chain"])
        return render_template('results.html',result=result["chain"])
        
    print("this is the chain details i guess")
    print(posts)
    print("let me check")
    return render_template('results.html')
    
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=="POST":
        #get fields
        username=request.form['username']
        password=request.form['password']
        send_object={
                'name': username,
        'password': password,
                }
        check_login_address = "{}/check_login".format(CONNECTED_NODE_ADDRESS)
        
        ans=requests.post(check_login_address,
                  json=send_object,
                  headers={'Content-type': 'application/json'})
        print("status code from server for post request",ans.status_code)
        print("now sending get request")
        
        if ans.status_code == 201:
            session['logged_in']=True
            session['username']=username
            flash('You are now logged in','success')
            app.logger.info("PASSWORD MATCH")
            return redirect(url_for('dashboard'))
    
        else:
            app.logger.info("INVALID CREDITIONALS")
            error="INVALID CREDITIONALS"
            return render_template('login.html',error=error)
        
    return render_template('login.html')   

@app.route('/logout')
def logout():
    session.clear()
    flash('You are now logged out','success')
    return redirect(url_for('login'))

def is_logged_in(f):
    @wraps(f)
    def wrap(*args,**kwargs):
        if 'logged_in' in session:
            return f(*args,**kwargs)
        else:
            flash('unautharised, please login','danger')
            return redirect(url_for('login'))
    return wrap

@app.route('/dashboard')
@is_logged_in
def dashboard():
    get_mem_address = "{}/get_mem".format(CONNECTED_NODE_ADDRESS)
    response = requests.get(get_mem_address)
    if response.status_code == 200:
        members = json.loads(response.content)
        print("if succesfull let me see")
        print(members["chain"])
        return render_template('dashboard.html',members=members["chain"])
        
    print("this is the chain details i guess")
    print(posts)
    print("let me check")
    return render_template('dashboard.html')

@app.route('/do_vote/<string:id>/',methods=['GET','POST'])
@is_logged_in
def do_vote(id):
    
    post_object = {
        'author': session['username'],
        'content':id
    }

    # Submit a transaction
    new_tx_address = "{}/new_transaction".format(CONNECTED_NODE_ADDRESS)

    hel=requests.post(new_tx_address,
                  json=post_object,
                  headers={'Content-type': 'application/json'})
    if(hel.status_code==404):
        flash("You have aldeardy voted ",'danger')
    else:
        flash("Thanks for voting",'success')
        
    return redirect('/')
    

def timestamp_to_string(epoch_time):
    return datetime.datetime.fromtimestamp(epoch_time).strftime('%H:%M')
