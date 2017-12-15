#!usr/local/bin/python

from flask import Flask, jsonify, request, make_response, abort, url_for
from flask_restful import Api, Resource, reqparse, fields, marshal

import sys
import os
import requests
import json

app = Flask(__name__)
api = Api(app)

nodes = []


#ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
# Enter a file in which to save the key (/Users/you/.ssh/id_rsa): [Press enter]i
# Enter passphrase (empty for no passphrase): [Type a passphrase]
# Enter same passphrase again: [Type passphrase again]
# keyContents = open(os.path.expanduser("~/.ssh/id_dsa.pub")).read()
# agh.repos.addDeployKey('myrepo', 'Key Name', keyContents)
#have to do error handling

# this will start the node
class start(Resource):
    def __inti__(self):
        super(start, self).__init__()
        global tasks 
        
    def get(self):
        #start master
        
        pass
    
    def post(self):
        #
        pass
api.add_resource(start, '/begin', endpoint = 'begin')


    

# This will delagaet jobs if there are any to give
class jobs(Resource):
    def __inti__(self):
        super(jobs, self).__init__()
        global tasks

    
    def get(self):
        #this will keep getting the next job to give to the node that is asking
        #if master has begun go and get the next job
        if tasks.begin == True:
            break
        pass
    
    def post(self):
        pass

api.add_resource(jobs, '/jobs', endpoint = 'jobs')

#This will resive the results and cal the overal avg
class ans(Resource):f
    def __init__(self):
        super(results, self).__init__()
        total = []
    
    def get(self):
        pass
    

api.add_resource(results, '/ans', endpoint = '/ans')

    

# This will control the main node .. task_setter
class task_setter():
    def __inti__(self, token):
        self.begin = False
        self.token = True
        self.repo = self.get_repo()
        self.repo_name = ""
        
        

    def get_repo(self):
        repo = git.Repo("")
        pass


    def run(self):
        pass

    def cal_avg(self):
        pass

    def total(self):
        pass

    def reo_trees(self):
        #need list of commits
        commits = requests.get(get_repo() + "/commits", params={'access_token' : self.token})
        #need list of all trees and file/ dirs in these trees
        #all of these gotten with tokens
        #using sha key -> get this from the commits
        trees = []
        commits_ = []
        for commit in commits_:
            sha = commit['sha']
            commits.append(sha)
            tree_url = get_repo() + "/trees/" + sha
            tree = request.get()
            



        pass



    # def deleteresults(self):
    #     pass





if __name__ == '__main__':
    tocken = ''
    tasks = task_setter()
    
    


