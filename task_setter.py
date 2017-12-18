#!/usr/local/bin/python

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


# ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
# Enter a file in which to save the key (/Users/you/.ssh/id_rsa): [Press enter]
# Enter passphrase (empty for no passphrase): [Type a passphrase]
# Enter same passphrase again: [Type passphrase again]
# keyContents = open(os.path.expanduser("~/.ssh/id_dsa.pub")).read()
# agh.repos.addDeployKey('myrepo', 'Key Name', keyContents)
# have to do error handling
# Get a tree -> repos/:owner/:repo/git/trees/:sha 
# Get a commit -> /repos/:owner/:repo/commits (list of commits in a repo )
# https://stackoverflow.com/questions/15919635/on-github-api-what-is-the-best-way-to-get-the-last-commit-message-associated-w
# token ae14a11eaefa3959d3aa11e4cc4abc5833dee4e3


# What the file does
# Spin up workers -> with comandline args
# Get files form git repo 
# Give jobs -> { Every commit -> count, Every tree -> count, file -> give with commit, path, url }
# Job Response -> done with file store ans
# Results -> { add up, Get avg, kill task_setter }



# This will delagaet jobs if there are any to give

class jobs(Resource):
    def __inti__(self):
        super(jobs, self).__init__()
        global test

    # this will give the task 
    def get(self):
        job_, _file, _commit = test.get_job()
        if job_ == 'finsihed':
            return {'URL' : 'finsihed'}
        return {'URL': job_, 'COMMIT': _commit, 'PATH', _file}

    # This will resive the ans 
    def post(self):
        # get info form ans
        requ = request.json() # this is what the worker sent the master
        must_haves = ['URL', 'AVERAGE', 'COMMIT', 'PATH']
        ans_ = []
        for items in must_haves:
            ans_.append(requ[items])
        test.results(ans_)


api.add_resource(jobs, '/jobs', endpoint='jobs')


# This will control the main node .. task_setter

class task_setter():
    def __inti__(self, gitname, reponame):
        global begin
        self.token = self.get_token()
        self.repo = self.get_repo(gitname, reponame)
        self.commits = []
        self.trees = {}
        self.commit_number = 0

    def get_token(self):
        with open("Tokens.txt", "r") as _file:
            return _file.read().split()[0]
        
    def get_repo(self, gitname, reponame):
        address = "https://api.github.com.repos" + str(gitname) + "/" + str(reponame)
        return address

    def get_trees(self):
        print("getting trees")
        commits = requests.get(self.repo + "/commits", params={"access_token":str(self.token)}).json()
        trees = {}
        commits_ = []
        for commit in commits:
            sha = commit['sha']
            commits_.append(sha)
            tree_url = self.repo + "/git/trees/" + str(sha)
            tree = requests.get(tree_url, params={"access_tocken":str(self.token),"recursive": 1}).json()
            print(tree)
            if 'tree' in tree:
                new = []
                for info in tree['tree']:
                    new.append(info)
                trees[sha] = new
            else:
                print("I would say you went ober the API rate limit!")
        return trees, commits_



    # TODO: need to thread this!
    def run(self):
        # start up a job class 
        







    #testing one file
    # get all files
    # give file to worker
    # when of laoded remove the file
    # increment the commit 
    def get_job(self):
        if self.commit_number < len(self.commits):
            for commit in self.commits:




        # NOTE: Testing section
        commit = self.commit[0] #sha commmit
        tree = self.trees[commit]  #list of files
        dets = tree[0]  # details about that file
        return dets['url'], dets['path'], commit

    def results(self, ans_):
        pass


    def cal_avg(self):
        pass

    def total(self):
        pass


                             


if __name__ == '__main__':
    # arg 1 - git name
    # arg 2 - it repo
    # arg 3 - number of nodes
    begin = False
    tasks = task_setter(sys.argv[1], sys.argv[2])
    tasks.run()
    # spinning up the number of nodes
    for i in range(sys.argv[3]):
        print(i, ": ", os.system('./node.py' + ' ' str(sys.argv[1]) + ' ' + sys.argv[2]))
    


app.run(host='0.0.0.0', debug=True, port=5050)

    
    


