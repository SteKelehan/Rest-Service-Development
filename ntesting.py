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
from time import sleep
from pprint import pprint



class ntesting():
    def __init__(self, repo, gitname):
        self.begin = True
        self.name = gitname
        self.repo = repo
        self.rurl = "https://api.github.com/" + str(self.name) + str(self.repo)
        self.token = self.get_token() 
        self.job_address = 'http://localhost:5050/jobs'

    def get_job(self):
        # print("so im in here?")
        return requests.get(self.job_address).json()

    def get_token(self):
        with open("Tokens.txt", "r") as _file:
            return _file.read().split()[0]

    def give_ans(self, job, avg):
        # print(type(job))
        pprint(job)
        print(avg)
        # print(type(avg))
        return requests.post(self.job_address, json={'STATUS':job['STATUS'], 'AVERAGE':avg, 'COMMIT':job['COMMIT'], 'PATH':job['PATH']}).json()


# gets files
# repos/owner/repo/commits/sha -> raw url gives you contnest
    def get_file(self, job):
        payload = {'access_token': self.token}
        self.start = "https://raw.githubusercontent.com/"
        self.path = job['PATH']
        self.sha = job['COMMIT']
        self.url = self.start + self.name + '/' + self.repo + '/' + self.sha + '/' + self.path
        # print('url')
        # print(self.url)
        return requests.get(self.url, params=payload).text

  

    def calc_test(self, job):
        file_ = self.get_file(job)
        if "readme" in job["PATH"]:
            return 0
        complex_ = mi_parameters(file_)
        print (complex_[1])
        return complex_[1]

    def work(self):
        self.done = False
        # if does not have work get work
        while self.done is False:
            # ask for a job
            # TODO: if the response says no job -> sleep
            print("Getting job")
            job = self.get_job()
            print(job)
            # print("get to this point?")
            if "finished" in job["STATUS"]:
                self.done = True
                break
            if None in job:
                print("Task Setter not activated yet")
                sleep(5)
            # if it has work calcuate the avrage
            # print("cacl avg")
            average = self.calc_test(job)
            # when avrage is computeded send it back to task_setter
            print("sending avg back")
            print(type(job))
            pprint(job)
            self.give_ans(job, average)

if __name__ == '__main__':
    test = ntesting("testing", "SteKelehan")
    test.work()
