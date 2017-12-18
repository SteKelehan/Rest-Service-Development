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
    def __init__(self, repo, gitname):
        # inits vars
        self.name = gitname
        self.repo = repo
        self.rurl = "https://api.github.com/" + str(self.name) + str(self.repo)
        # Gets token to acess git from file
        self.token = self.get_token() 
        # This is the rest address tp send the requests to 
        self.job_address = 'http://localhost:5050/jobs'

    # This will give the worker a job
    def get_job(self):
        return requests.get(self.job_address).json()

    # This will retive the token form the text file
    def get_token(self):
        with open("Tokens.txt", "r") as _file:
            return _file.read().split()[0]

    # This function send the CC back to the task setter
    def give_ans(self, job, avg):
        # print(type(job))
        pprint(job)
        print(avg)
        # print(type(avg))
        return requests.post(self.job_address, json={'STATUS':job['STATUS'], 'AVERAGE':avg, 'COMMIT':job['COMMIT'], 'PATH':job['PATH']}).json()

    # This function pull the text info form git api
    def get_file(self, job):o
        # allows you access
        payload = {'access_token': self.token}
        # This is where the raw data in a file is on the git api
        self.start = "https://raw.githubusercontent.com/"
        self.path = job['PATH']
        self.sha = job['COMMIT']
        # give the info from the git repo this will genorate the url needed to extract the file data
        self.url = self.start + self.name + '/' + self.repo + '/' + self.sha + '/' + self.path
        # Returns the data in .txt 
        return requests.get(self.url, params=payload).text

  
    # This use radon to calc CC on file
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
                sleep(.5)
            # if it has work calcuate the avrage
            # print("cacl avg")
            average = self.calc_test(job)
            # when avrage is computeded send it back to task_setter
            print("sending avg back")
            print(type(job))
            pprint(job)
            self.give_ans(job, average)

if __name__ == '__main__':
    print("Node has started up!")
    node = Node(sys.argv[1], sys.argv[2])
    node.work()
