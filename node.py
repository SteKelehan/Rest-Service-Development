#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

from flask import Flask, jsonify, request, make_response, url_for
# from flask_restful import Api, Resource, reqparse, fields, marshal
from radon.complexity import SCORE
from radon.cli.harvest import CCHarvester
from radon.cli import Config
import time from sleep # TODO: add a sleeper to the node if there is no job to do
import os
# application/vnd.github.VERSION.raw -> retrive teh contents of the file
# This is going to calculate the avrage Complexity on the git hub commit!
# The head worker that delagates the taskes will give each worker a github rebo URL

# What the file dose
# Ask for Job
# If job -> { Get file from git(url), Cal complexity, Respond to ans -> reslut, Look for Job}
# If no job -> {responce will == sleep, sleep, Ask for job again}
# If jobs done -> {responce will == done , kill worker}


class Node():
    def __init__(self, gitname, repo):
        self.job_address = 'http://localhost:5000/job'
        self.send_address = 'http://localhost:5000/ans'
        self.name = gitname
        self.repo = repo
        self.rurl = "https://api.github.com/" + str(self.name) + str(self.repo)
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
        with open("Tokens.txt", "r") as _file:
            return _file.read().split()[0]

    # gets files
   
    def get_file(self, job):
        payload = {'access_token': self.token}
        self.start = "https://raw.githubusercontent.com"
        self.path = job['PATH']
        self.sha = job['COMMIT']
        self.url = self.start + self.name + self.repo + self.sha
        return request.get(self.url, params=payload).text

    # calcs the complexity
    # might be using a diffrent method!
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

     def calc_test(self, file_):
        complex_ = mi_parameters(file_)
        return complex_[1]

    # do work until no more work to be done
    def work(self):
        # if does not have work get work
        while self.done is not False:
            # ask for a job
            # TODO: if the response says no job -> sleep
            job = self.find_job()
            if "finished" in job:
                self.done = True
                break
            if job is None:
                sleep(0.5)
            else:
                # if it has work calcuate the avrage
                average = self.calcuate_avrage(job)
                # when avrage is computeded send it back to task_setter
                self.respond(average, job)


if __name__ == '__main__':
    print("Node has started up!")
    node = Node(sys.argv[1], sys.argv[2])
    node.work()
