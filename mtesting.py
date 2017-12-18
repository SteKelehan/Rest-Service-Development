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

class testing():
    ###################### WORKING! ###################### 
    def __init__(self):
        self.begin = True
        self.repo = "https://api.github.com/repos/SteKelehan/testing"
        global task 
        self.token = self.get_token()
        self.trees, self.commits= self.get_trees()
        self.paths = [] # put in init 
        self.commit_index = len(self.commits) - 1
        self.next_com = True
        self.path_index = 0
        self.resultsdic = {}

    def get_token(self):
        with open("Tokens.txt", "r") as _file:
            return _file.read().split()[0]

    def get_trees(self):
        print("getting trees")
        commits = requests.get(self.repo + "/commits", params={"access_token":str(self.token)}).json()
        trees = {}
        commits_ = []
        for commit in commits:
            sha = commit['sha']
            commits_.append(sha)
            tree_url = self.repo + "/git/trees/" + str(sha)
            tree = requests.get(tree_url, params={"access_token":str(self.token),"recursive": 1}).json()
            # print(tree)
            self.count = 0
            if 'tree' in tree:
                new = []
                for info in tree['tree']:
                    if info['type'] == 'blob':
                        new.append(info)
                        self.count += 1
                trees[sha] = new
            else:
                print("I would say you went ober the API rate limit!")
            print ("Count: ", self.count)
        print(len(trees))
        print(len(trees.keys()))
        return trees, commits_
    
    def results(self, responce):
        self.com = responce["COMMIT"]
        self.ans = responce["AVERAGE"]
        self.resultsdic[self.com].extend([self.ans])
        

    def print_to_file(self):
        #clacs the avg and puts in file
        new = {k: sum(v)/len(v) for k, v in dic.items() if len(v) > 0}
        with open("Results.txt", "w") as f:
            f.write(json.dumps(new))

    def get_job(self):
        # in each commit calculate the complexit -> avg
        # in each commit there is trees  
        # in each commit send the file to a worker to calc complex
        # when commit avg complete send to file

        if self.commit_index < 0:
            print("Finsihed Repo")
            return "finished", None, None
        else:
            self.curr_commit = self.commits[self.commit_index]
            if self.path_index  == len(self.paths):
                self.commit_index -= 1
                self.next_com = True
            if self.next_com is True:
                print("Starting Tree")
                self.paths = []
                # print("Paths", self.paths)
                self.path_index = 0
                for item in self.trees[self.curr_commit]:
                    self.paths.append(item['path'])
                # print("Paths now: ", self.paths)
                self.next_com = False
            
            commit = self.curr_commit
            url = "dont know if i need it yet!"
            # print("Paths index: ", self.path_index)
            path = self.paths[self.path_index]
            self.path_index += 1
            # print("Lenght of paths", len(self.paths))
            # print c("STATUS: ", url)
            print("COMMIT: ", commit)
            print("PATH", path)
        return url, commit, path 


        

class jobs(Resource):
    def __inti__(self):
        super(jobs, self).__init__()
        global test

    # this will give the task 
    def get(self):
        print('Getting a Job!')
        job_, _commit, _file = test.get_job()
        if job_ == 'finsihed':
            return {'STATUS' : 'finsihed'}.json()
        return {'STATUS': job_, 'COMMIT': _commit, 'PATH': _file}

    # This will resive the ans 
    def post(self):
        print("Resiving a Job")
        r = request.json
        must_haves = ['STATUS', 'AVERAGE', 'COMMIT', 'PATH']
        ans_ = []
        for items in must_haves:
            ans_.append(r[items])
        test.results(ans_)

api.add_resource(jobs, '/jobs', endpoint='jobs')




if __name__ == '__main__':
    test = testing()
    # print("commtis")
    # print(test.commits)
    # print("trees:")
    # print(test.trees)
    app.run(host='0.0.0.0', debug=True, port=5050)


                
