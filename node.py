#!/usr/local/bin/python3

from flask import Flask, jsonify, request, make_response, abort, url_for
# from flask_restful import Api, Resource, reqparse, fields, marshal
from radon.complexity import SCORE
from radon.cli.harvest import CCHarvester
from radon.cli import Config
# import sys
# import os
# import requests
# import json

# application/vnd.github.VERSION.raw -> retrive teh contents of the file
# This is going to calculate the avrage Complexity on the git hub commit!
# The head worker that delagates the taskes will give each worker a github rebo URL


class Node():
    def __init__(self):
        self.job_address = 'http://localhost:5000/job'
        self.send_address = 'http://localhost:5000/ans'
        self.done = False
        self.token = self.get_token()
        self.configeration = Config(
            exclude="",
            ignore="",
            order=SCORE,
            no_assert=True,
            show_closure=False,
            min='A',
            max='F',
        )

    # Asks for job of task_setter
    def find_job(self):
        # Ask for a job this will return a json dic with URL, Commitment and the path
        job = request.get(self.job_address).json()
        return job

    # gives answer back to task setter
    def respond(self, average, job):
        return request.post(
            self.send_address,
            json={
                'URL': job["URL"],
                'AVERAGE': average,
                'COMMIT': job["COMMIT"],
                'PATH': job["PATH"]
            }).json()

    # returns the token
    def get_token(self):
        with open("Tokens", "r") as _file:
            return _file.read().split()[0]

    # gets files
    def get_file(self, job):
        payload = {'access_token': self.token}
        headers = {'Accept': 'application/vnd.github.v3.raw'}
        # creates a file with the name of the commit
        files = './temp/{}.py'.format(job["COMMIT"])
        with open(files, 'w') as _file:
            _file.write(
                request.get(job["COMMIT"], params=payload,
                            headers=headers).text)
        return _file

    # calcs the complexity
    # http://radon.readthedocs.io/en/latest/api.html
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

    # do work until no more work to be done
    def work(self):
        # if does not have work get work
        while self.done == False:
            # ask for a job
            job = self.find_job()
            # if it has work calcuate the avrage
            average = self.calcuate_avrage(job)
            # when avrage is computeded send it back to task_setter
            self.respond(average, job)
            if "finished" in job:
                self.done = True
                break


if __name__ == '__main__':
    node = Node()
    node.work()
