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
    def __init__(self):
        self.begin = True
        self.repo = "https://api.github.com/repos/SteKelehan/testing"
        global task 
        self.token = "ae14a11eaefa3959d3aa11e4cc4abc5833dee4e3"


    def run(self):
        print("waiting to start")
        while self.begin == False:
            if self.begin == True:
                print("Starting")
                # self.task.run()
                return

    def task_setter(self):
        pass


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

        
    def files(self):
        self.trees, self.commits = self.get_trees()    
        for sha in self.trees:
            print ("sha:", sha)
            for file_details in self.trees[sha]:
                print ("file: {} ({})".format(file_details["path"], file_details["url"]))

    
    
class jobs(Resource):
    def __inti__(self):
        super(jobs, self).__init__()
        global begin

    
    def get(self):
        
        pass
    
    def post(self):
        pass

api.add_resource(jobs, '/jobs', endpoint = 'jobs')




if __name__ == '__main__':
    # task = task_setter()
    # task.run()
    
    print('im in the main')
    test = testing()
    print(test.repo)
    test.get_trees()
    print(sys.argv[1])
    print(test.get_token())
    for i in range(int(sys.argv[1])):
        t = threading.Thread(name='i',target=test.run())
        t.start()        
    test.files()


                
