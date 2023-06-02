#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import hashlib
import requests
from flask import render_template, redirect, request
import time
from flask import Flask, request
import requests
import datetime
import json
from flask import Flask,render_template,request,flash,redirect,url_for,session,logging
import wtforms
from wtforms import Form,StringField,TextAreaField,PasswordField,validators 
from passlib.hash import sha256_crypt
from functools import wraps



chain_state={}

#hash the transaction
def hash_function(k):
    """Hashes our transaction."""
    if type(k) is not str:
        k = json.dumps(k, sort_keys=True)
        print(k)
    else:
        k.encode('utf-8')
        print("a str")
        print(k)
     
    print("present hash is", hashlib.sha256((k).encode('utf-8')).hexdigest())
    return hashlib.sha256((k).encode('utf-8')).hexdigest()

#updating the status
def update_state(transaction, state):
    state = state.copy()

    for key in transaction:
        if key in state.keys():
            state[key] += transaction[key]
        else:
            state[key] = transaction[key]

    return state

#checking whether a valid transaction is there or not
def valid_transaction(transaction, state):
    """A valid transaction must sum to 0 becase if a person votes then the candidate 
    must get that vote"""
    if sum(transaction.values()) is not 0:
        return False

    for key in transaction.keys():
        if key in state.keys():
            account_balance = state[key]
        else:
            account_balance = 0

        if account_balance + transaction[key] < 0:
            return False

    return True


#making a block
def make_block(transactions, chain):
    """Make a block to go into the chain."""
    parent_hash = chain[-1]['hash']
    block_number = chain[-1]['contents']['block_number'] + 1

    block_contents = {
        'block_number': block_number,
        'parent_hash': parent_hash,
        'transaction_count': block_number + 1,
        'transaction': transactions
    }

    return {'hash': hash_function(block_contents), 'contents': block_contents}

#check whether the block is valid or not
def check_block_hash(block):
    expected_hash = hash_function(block['contents'])

    if block['hash'] is not expected_hash:
        raise

    return


#check validity of block
def check_block_validity(block, parent, state):
    parent_number = parent['contents']['block_number']
    parent_hash = parent['hash']
    block_number = block['contents']['block_number']

    for transaction in block['contents']['transaction']:
        if valid_transaction(transaction, state):
            state = update_state(transaction, state)
        else:
            raise

    check_block_hash(block)  # Check hash integrity

    if block_number is not parent_number + 1:
        raise

    if block['contents']['parent_hash'] is not parent_hash:
        raise

    return state

#checking the chain
def check_chain(chain):
    """Check the chain is valid."""
    if type(chain) is str:
        try:
            chain = json.loads(chain)
            assert (type(chain) == list)
        except ValueError:
            # String passed in was not valid JSON
            return False
    elif type(chain) is not list:
        return False

    state = {}

    for transaction in chain[0]['contents']['transaction']:
        state = update_state(transaction, state)

    check_block_hash(chain[0])
    parent = chain[0]

    for block in chain[1:]:
        state = check_block_validity(block, parent, state)
        parent = block

    return state

#adding transaction to chain
def add_transaction_to_chain(transaction, state, chain):
    if valid_transaction(transaction, state):
        state = update_state(transaction, state)
    else:
        print ('Alderady voted !!! Can\'t vote again')
        return state, chain

    my_block = make_block(state, chain)
    chain.append(my_block)

    for transaction in chain:
        check_chain(transaction)

    return state, chain


#ditionary for a block
genesis_block = {
    'hash': hash_function({
        'block_number': 0,
        'parent_hash': None,
        'transaction_count': 1,
        'transaction': []
    }),
    'contents': {
        'block_number': 0,
        'parent_hash': None,
        'transaction_count': 1,
        'transaction': []
    },
}
    
#add voter to chain by creating a block for him    
def add_voter_to_chain(f,chain_st):
    for i in f:
        name=i
        vote=1
        chain_st[name]=vote
    return chain_st
#add candidate to chain by creating a block for him
def add_member_to_chain(m,chain_st):
    for i in m:
        name=i
        vote=0
        chain_st[name]=vote
    return chain_st

#block chain
block_chain = [genesis_block]


#function for voting 
def do_vote(cand,vote):
    global chain_state
    global block_chain
    chain_state, block_chain = add_transaction_to_chain(transaction={vote: -1, cand: 1}, state=chain_state, chain=block_chain)

#a list for voters
voters=[]
# a list for voters
canditiates=['N. Chandra Babu Naidu','Y. S. Jagan Mohan Reddy', 'K. Pavan Kalyan']
chain_state=add_voter_to_chain(voters,chain_state)
chain_state=add_member_to_chain(canditiates,chain_state)

#making my server

app = Flask(__name__)

#dictionary for users details
users={}
# the address to other participating members of the network
#if many network are there
peers = set()

@app.route('/register_server',methods=['POST'])
def register():
    user_data=request.get_json()
    print("values")
    print(user_data["name"])
    print(user_data["password"])
        
    users[user_data['name']]=user_data['password']
    print("full ditionary once",users)
    vot=[user_data["name"]]
    global voters
    voters.append(user_data["name"])
    global chain_state
    chain_state=add_voter_to_chain(vot,chain_state)
    print("chain state prinitng",chain_state)
    return "Success",201

# endpoint to submit a new transaction. This will be used by
# our application to add new data (posts) to the blockchain

@app.route('/new_transaction', methods=['POST'])
def new_transaction():
    
    tx_data = request.get_json()
    required_fields = ["author", "content"]
    if(chain_state[tx_data['author']]==0):
        print("aldeardy voted")
        return "error",404
    for field in required_fields:
        if not tx_data.get(field):
            return "Invlaid transaction data", 404

    tx_data["timestamp"] = time.time()
    print("inside new_transaction ")
    print("candidate ",canditiates[int(tx_data["content"])])
    print("voter ",tx_data["author"])
    do_vote(canditiates[int(tx_data["content"])],tx_data["author"])

    return "Success", 201

# endpoint to return the node's copy of the chain.
# Our application will be using this endpoint to query
# all the posts to display.

#check whther the login is correct not
@app.route('/check_login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        login_data=request.get_json()
        username=login_data["name"]
        print("inside login function server")
        if(sha256_crypt.verify(login_data["password"],users[username])):
           print("both matching")
           return "success",201
        return "error",404
    
    
    
    
votes_sum=0

#check the state of block chain        
@app.route('/get_result',methods=['GET'])
def get_result():
    ans=[]
    global votes_sum
    for person in voters:
        if(chain_state[person]==0):
            votes_sum=votes_sum+1
    for name in canditiates:
        di={}
        di['name']=name
        di['votes']=chain_state[name]
        
        
        di['per']=((int(chain_state[name]))/(len(voters)))
        di['total']=len(voters)
        di['present']=votes_sum
        ans.append(di)
    return json.dumps({"length": len(ans),
                       "chain": ans})    



    
@app.route('/fetch_name')
def fetch_name():
    for block in block_chain:
        print(block['contents']['transaction'])



#get the list of all candidates along with their id
@app.route('/get_mem',methods=['GET'])
def get_name():
    ans=[]
    count=0;
    for i in canditiates:
        p={}
        p['id']=count
        p['name']=i 
        ans.append(p)
        count=count+1   
    return json.dumps({"length": count,
                       "chain": ans})


@app.route('/chain', methods=['GET'])
def get_chain():
    # make sure we've the longest chain
    
    chain_data = []
    for block in block_chain:
        chain_data.append(block)
    return json.dumps({"length": len(chain_data),
                       "chain": chain_data})
    
app.run(debug=True, port=8000)