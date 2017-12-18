#!/usr/local/bin/python

from flask import Flask, jsonify, request, make_response, abort, url_for
from flask_restful import Api, Resource, reqparse, fields, marshal

import sys
import os
import requests
import json
import pprint
import threading
from radon.complexity import SCORE, cc_rank, cc_visit
from radon.cli.harvest import CCHarvester
from radon.metrics import mi_parameters
from radon.cli import Config


app = Flask(__name__)
api = Api(app)


class ntesting():
    def __init__(self, repo, gitname):
        self.begin = True
        self.name = gitname
        self.repo = repo
        self.rurl = "https://api.github.com/" + str(self.name) + str(self.repo)
        self.token = self.get_token() 
        self.configeration = Config(
            exclude="",
            ignore="",
            order=SCORE,
            no_assert=True,
            average=True,
            total_average=True,
            show_closure=False,
            min='A',
            max='F',
        )
        self.job_address = 'http://localhost:5000/job'

    def get_job(self):
        return request.get(self.job_address).json()

    def get_token(self):
        with open("Tokens.txt", "r") as _file:
            return _file.read().split()[0]


# gets files
# repos/owner/repo/commits/sha -> raw url gives you contnest
    def get_file(self, job):
        payload = {'access_token': self.token}
        self.start = "https://raw.githubusercontent.com/"
        self.path = job['PATH']
        self.sha = job['COMMIT']
        self.url = self.start + self.name + '/' + self.repo + '/' + self.sha + '/' + self.path
        return request.get(self.url, params=payload).text

    def calcuate_avrage(self):
        # f = self.get_file(job)
        url = "https://raw.githubusercontent.com/SteKelehan/testing/53fba9a79b063f636ece5ee0545986d3d3bc0716/test.py"
        f = requests.get(url, params={"access_token":str(test.token)}).text
        # computing the complexioty
        # This will return a tuple in formate (line, args, kwargs)
        results = CCHarvester([f], self.configeration).to_terminal()
        # extract avg from results
        for result in results:
            line, args, kwargs = result[0], result[1], result[2]
            if type(line) == str:
                if "Average complexity:" in line:
                    avg = args[2]
                    print ("AVG", avg)
                    return avg


    def calc_test(self):
        file_ = self.get_file()
        complex_ = mi_parameters(file_)
        return complex_[1]


   
    def work(self):
        self.done = False
        # if does not have work get work
        while self.done is not False:
            # ask for a job
            # TODO: if the response says no job -> sleep
            job = self.get_job()
            if "finished" in job:
                self.done = True
                break
            # if it has work calcuate the avrage
            average = self.calc_test(job)
            # when avrage is computeded send it back to task_setter
            self.respond(average, job)

if __name__ == '__main__':
    test = ntesting("SteKelehan", "testing")
    test.work()
    # job = {"url":"https://api.github.com/repos/SteKelehan/testing/git/blobs/e69de29bb2d1d6434b8b29ae775ad8c2e48c5391", 
    #         "commit" : 1 , 
    #         "Path": "test.py"}
    # job = test.get_job()
    # print(request.get_file(job))    # print(test.calcuate_avrage(job))
    # with open("node.py","r") as f:
        # data = f.read()
    # print(data)

    # url = "https://raw.githubusercontent.com/SteKelehan/testing/53fba9a79b063f636ece5ee0545986d3d3bc0716/test.py"
    # x = requests.get(url, params={"access_token":str(test.token)}).text
    # print (x)
    # y = test.calc_test(x)
    # print("y: ", y)
    # z = test.calcuate_avrage()
    # print(z)
    # print(test.get_file(url))
    # result = test.calc_test(data)  
    # result = test.calc_test(data)  
    # print("Result: ", result)
    # test.get_job()
    # print (test.calc_test())

