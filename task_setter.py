#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, jsonify, request, make_response, url_for
from flask_restful import Api, Resource, reqparse, fields, marshal

import requests
import threading
import json
from collections import defaultdict

app = Flask(__name__)
api = Api(app)



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
# Get file info form git repo 
# Give jobs -> { Every commit -> count, Every tree -> count, file -> give with commit, path, url }
# Job Response -> done with file store ans
# Results -> { add up, Get avg, kill task_setter }



class task_setter(gitname, gitrepo):
    def __init__(self):
        # Init vars
        self.name = gitname
        self.gitrepo = gitrepo 
        self.repo = "https://api.github.com/repos/" + str(gitname) + "/" + str(gitrepo) + "/"
        # Token to access git repo
        self.token = self.get_token()
        # pull all the data for trees and commits from choosen repo 
        self.trees, self.commits= self.get_trees()
        # this is for all the file name of a given repo when give jobs to nodes
        self.paths = []
        # The next vars keeping take of commits/paths and results when hading jobs to workers
        self.commit_index = len(self.commits) - 1
        self.next_com = True
        self.path_index = 0
        self.resultsdic = {}
        # allowing the rest of the class to access the task obj (not great convenstion)
        global task 

    # Gets token from file
    def get_token(self):
        with open("Tokens.txt", "r") as _file:
            return _file.read().split()[0]

    # Gets info from git api - keep a list of commits and the trees in a given commit
    def get_trees(self):r
        print("getting trees")
        # Get commits
        commits = requests.get(self.repo + "/commits", params={"access_token":str(self.token)}).json()
        trees = {}
        commits_ = []
        # Each commit has a sha - retive and thats stored in commits list
        for commit in commits:
            sha = commit['sha']
            commits_.append(sha)
            tree_url = self.repo + "/git/trees/" + str(sha)
            # Get trees for each commit 
            tree = requests.get(tree_url, params={"access_token":str(self.token),"recursive": 1}).json()
            if 'tree' in tree:
                new = []
                # But only take the info if its a blob - meaning its a file not a dir with more files
                for info in tree['tree']:
                    if info['type'] == 'blob':
                        new.append(info)
                trees[sha] = new
            else:
                print("I would say you went over the API rate limit!")
        return trees, commits_
    
    # This adds up the results and stors the info in a dic (key - sha)
    def results(self, responce):
        self.com = responce["COMMIT"]
        self.ans = responce["AVERAGE"]
        self.resultsdic[self.com].extend([self.ans])
        
    # Prints the result to a text file 
    def print_to_file(self):
        #clacs the avg and puts in file
        new = {k: sum(v)/len(v) for k, v in dic.items() if len(v) > 0}
        with open("Results.txt", "w") as f:
            f.write(json.dumps(new))

    # It gives a job to a node that is asking
    # Returns a status (meaign if the status is fisihed it will send finsihed), the path (filename), commit (sha)
     def get_job(self):
        # Each commit calculate the complexit -> avg in each commit there is trees  in each commit send the file to a worker to calc complex
        # If there is no more commits kill the workers  
        if self.commit_index < 0:
            print("Finsihed Repo")
            return "finished", None, None
        else:
            # Check to see if there is paths left in commit if so index to next path else move to next comtit
            self.curr_commit = self.commits[self.commit_index]
            if self.path_index == len(self.paths):
                self.commit_index -= 1
                self.next_com = True
            if self.next_com is True:
                self.paths = []
                self.path_index = 0
                for item in self.trees[self.curr_commit]:
                    self.paths.append(item['path'])
                self.next_com = False
            
            commit = self.curr_commit
            status = "done"
            path = self.paths[self.path_index]
            self.path_index += 1
        return status, commit, path 

        
# This is an API class this calls itself so it can reived request and send when requested
class jobs(Resource):
    def __inti__(self):
        super(jobs, self).__init__()
        # This was made globe in order to acess its functions
        global test

    # This will give the task 
    def get(self):
        print('Getting a Job!')
        # calls the job getter above and give it to the node
        job_, _commit, _file = test.get_job()
        if job_ == 'finsihed':
            return {'STATUS' : 'finsihed'}.json()
        return {'STATUS': job_, 'COMMIT': _commit, 'PATH': _file}

    # This will resive the ans from node and call the results to add it to tolal commit complexity form a given node
    def post(self):
        print("Resiving a Job")
        # resives job
        r = request.json
        must_haves = ['STATUS', 'AVERAGE', 'COMMIT', 'PATH']
        ans_ = []
        # Appends itesm to list and sends it to results above
        for items in must_haves:
            ans_.append(r[items])
        test.results(ans_)

# This is here to access the endpoints 
api.add_resource(jobs, '/jobs', endpoint='jobs')

if __name__ == '__main__':
    # arg 1 - git name
    # arg 2 - it repo
    # arg 3 - number of nodes

    tasks = task_setter(sys.argv[1], sys.argv[2])
    tasks.run()
    # spinning up the number of nodes
    for i in range(sys.argv[3]):
        print(i, ": ", os.system('./node.py' + ' ' str(sys.argv[1]) + ' ' + sys.argv[2]))
    app.run(host='0.0.0.0', debug=True, port=5050)

    
    


