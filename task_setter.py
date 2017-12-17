#!usr/local/bin/python

from flask import Flask, jsonify, request, make_response, abort, url_for
from flask_restful import Api, Resource, reqparse, fields, marshal

import sys
import os
import requests
import json
import threads 

app = Flask(__name__)
api = Api(app)

threads = []
nodes = []


#ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
# Enter a file in which to save the key (/Users/you/.ssh/id_rsa): [Press enter]i
# Enter passphrase (empty for no passphrase): [Type a passphrase]
# Enter same passphrase again: [Type passphrase again]
# keyContents = open(os.path.expanduser("~/.ssh/id_dsa.pub")).read()
# agh.repos.addDeployKey('myrepo', 'Key Name', keyContents)
#have to do error handling
# Get a tree -> repos/:owner/:repo/git/trees/:sha 
# Get a commit -> /repos/:owner/:repo/commits (list of commits in a repo )
# https://stackoverflow.com/questions/15919635/on-github-api-what-is-the-best-way-to-get-the-last-commit-message-associated-w
# token ae14a11eaefa3959d3aa11e4cc4abc5833dee4e3

# This will delagaet jobs if there are any to give
class jobs(Resource):)
    def __inti__(self):
        super(jobs, self).__init__()
        global begin
        global test

    
    def get(self):
        #this will keep getting the next job to give to the node that is asking
        #if master has begun go and get the next job
        # if tasks.begin == True:
        #     breakA
        
        pass

    
    def post(self):
        job_, _file, _commit = test.get_job()
        return {'url': job_, 'commit', 'path', _file}

api.add_resource(jobs, '/jobs', endpoint = 'jobs')

#This will resive the results and cal the overal avg
class ans(Resource):
    def __init__(self):
        super(ans, self).__init__()     
        global begin
        total = []
    
    def get(self):
        pass
    

api.add_resource(ans, '/ans', endpoint = '/ans')

    

# This will control the main node .. task_setter
class task_setter():
    def __inti__(self, nodes):
        global begin
        self.token = self.get_token()
        self.repo = self.get_repo("SteKelehan")
        self.commits = []
        self.trees = {}
        self.commit_number = 0
        self.nodes = nodes

        
    def get_repo(self, gitname):
        address = "https://api.github.com.repos" + str(gitname) + "/" + "testing"
        return address

    def run(self):
        self.trees, self.commits = self.repo_trees()
    
    #testing one file
    def get_job(self):
        commit = self.commit[0] #sha commmit
        tree = self.trees[commit]  #list of files
        dets = tree[0]  # details about that file
        return dets['url'], dets['path'], commit

                
        

        pass

    def cal_avg(self):
        pass

    def total(self):
        pass

    def get_token(self):
        with open("Tokens.txt", "r") as _file:
            return _file.read().split()[0]

    def repo_trees(self):
        print("getting trees")
        commits = requests.get(self.repo + "/commits", params={"access_token":str(self.token)}).json()
        #need list of all trees and file/ dirs in these trees
        #all of these gotten with tokens
        #using sha key -> get this from the commits
        # Each repo has a list of folders in each commit know as trees each tree can contain more trees or blobs -> pure file
        trees = {}
        # Each commit is stroed in a list and each tree info for each commit are stored in a dic with the key being the sha!
        commits_ = []
        for commit in commits:
            sha = commit['sha']
            commits_.append(sha)
            tree_url = self.repo + "/git/trees/" + str(sha)
            # this request returns a list of all the repos trees in a given commit
            # print(tree_url)
            tree = requests.get(tree_url, params={"access_tocken":str(self.token),"recursive": 1}).json()
            # print(tree)
            if 'tree' in tree:
                new = []
                for info in tree['tree']:
                    new.append(info)
            trees[sha] = new
        print("trees: ")
        print(trees)
        print("Commits: ")
        print(commits_)
        return trees, commits_
                             


if __name__ == '__main__':
    tocken = ''
    begin = False
    tasks = task_setter(sys.argv[1])
    if sys.argv[2] == "y":
        tasks.run(sys.argv[1])
        begin = True
    else:
        return


    
    


