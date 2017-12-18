#!/usr/local/bin/python

from flask import Flask, jsonify, request, make_response, abort, url_for
from flask_restful import Api, Resource, reqparse, fields, marshal

import sys
import os
import requests
import json
import pprint
import threading

app = Flask(__name__)
api = Api(app)

class testing():
    ###################### WORKING! ###################### 
    def __init__(self):
        self.begin = True
        self.repo = "https://api.github.com/repos/SteKelehan/testing"
        global task 
        self.token = self.get_token()
        self.commits, self.trees = self.get_trees()

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
            if 'tree' in tree:
                new = []
                for info in tree['tree']:
                    new.append(info)
                trees[sha] = new
            else:
                print("I would say you went ober the API rate limit!")
        return trees, commits_


    def get_job(self):
        return 


    def test_job(self):
        return "someurl", "53fba9a79b063f636ece5ee0545986d3d3bc0716", "test.py"


        

class jobs(Resource):
    def __inti__(self):
        self.req = reqparse.RequestParser()
        self.req.add_argument('URL', type=str, location='json')
        self.req.add_argument('AVERAGE', type=str, location='json')
        self.req.add_argument('COMMIT', type=str, location='json')
        self.req.add_argument('PATH', type=str, location='json')

        super(jobs, self).__init__()
        global test

    # this will give the task 
    def get(self):
        job_, _file, _commit = test.test_job()
        if job_ == 'finsihed':
            return {'URL' : 'finsihed'}
        return {'URL': job_, 'COMMIT': _commit, 'PATH': _file}

    # This will resive the ans 
    def post(self):
        # get info form ans
        # requ = request.json() # this is what the worker sent the master
        # r = request
        # print(r)A
        args  = self.req.parse_args()
        must_haves = ['URL', 'AVERAGE', 'COMMIT', 'PATH']
        ans_ = []
        for items in must_haves:
            ans_.append(args[items])
        test.results(ans_)

api.add_resource(jobs, '/jobs', endpoint='jobs')




if __name__ == '__main__':
    # task = task_setter()
    # task.run()
    
    # print('im in the main')
    test = testing()
    Job = jobs()
    Job.get()
    # print(test.repo)
    # test.get_trees()
    # print(sys.argv[1])
    # print(test.get_token())
    # for i in range(int(sys.argv[1])):
        # t = threading.Thread(name='i',target=test.run())
        # t.start()        
    # test.files()

    # Job = jobs()
    # Job.post()
    # print(test.commits)
    # print(test.trees)
    # print(test.commits[0])A

    # Job.test_post()

    
app.run(host='0.0.0.0', debug=True, port=5000)


                
