#!/usr/local/bin/python

from flask import Flask, jsonify, request, make_response, abort, url_for
from flask_restful import Api, Resource, reqparse, fields, marshal

import sys
import os
import requests
import json
import pprint
import threading
from radon.complexity import SCORE
from radon.cli.harvest import CCHarvester
from radon.cli import Config


app = Flask(__name__)
api = Api(app)


class ntesting():
    def __init__(self):
        self.begin = True
        self.repo = "https://api.github.com/repos/SteKelehan/testing"
        self.token = "ae14a11eaefa3959d3aa11e4cc4abc5833dee4e3"
        self.configeration = Config(
            exclude="",
            ignore="",
            order=SCORE,
            no_assert=True,
            show_closure=False,
            min='A',
            max='F',
        )
        self.job_address = 'http://localhost:5000/job'

    def get_job(self):
        return request.get(self.job_address).json()


# gets files
    def get_file(self, job):
        payload = {'access_token': self.token}
        headers = {'Accept': 'application/vnd.github.v3.raw'}
        # creates a file with the name of the commit
        # files =job["Path"]
        # with open(files, 'w') as _file:
        #     _file.write(
        #         request.get(job["Path"], params=payload,
        #                     headers=headers).text)
        return request.get(job["url"], params=payload, headers=headers).json()

    def calcuate_avrage(self, job):
        f = self.get_file(job)
        # computing the complexioty
        # This will return a tuple in formate (line, args, kwargs)
        complexities = CCHarvester([f], self.configeration)
        for complexity in complexities:
            line, args, kwargs = complexity[0], complexity[1], complexity[2]
            if type(line) == str:
                if "Average complexity: " in line:
                    return args[2]


if __name__ == '__main__':
    test = ntesting()
    # job = {"url":"https://api.github.com/repos/SteKelehan/testing/git/blobs/e69de29bb2d1d6434b8b29ae775ad8c2e48c5391", 
    #         "commit" : 1 , 
    #         "Path": "test.py"}
    job = test.get_job()
    print(request.get_file(job))    # print(test.calcuate_avrage(job))
    
