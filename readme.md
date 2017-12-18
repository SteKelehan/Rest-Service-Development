# Internet App Cyclomatic Complexity

Student Name: Stephen Kelehan<br />
Student Number: 14316006<br />

## Project

This project was to construct a REST serves system, that would compute the code complexit for a give Git Repo. The instructions outlines use to build such a system that will run a number of nodes to decrease the exicution time by spreading the computation accorss mutiple nodes.


## Running the code  

The project was written in python. The repo contains 2 python files "task_master.py" and "node.py" these will be exicuting the caculation on the given repo. <br /> 
The repo also has a file called "Token.txt" this is where the git access token should be stored. <br />
There is a "makeenv.sh". This is the file that will install the nessasary python plug-ins.<br />
Finally there is a scrip called "setup.sh" that will take 3 comandline args 1.name of gitname, 2. name of repo and 3. the amout of nodes you would like to run on the repo.


## Code

There are two python scrips:

### task_setter.py

The files used a RESTful api to communicated with one another. The "task_maser.py" pulled the appropeate infomation from the choosen gitgub repo. It did this using the github API. The file is given asscess to the repo via github access tokens witch are stored ona "Token.txt" file.<br />
With this the scriped gets the commits and the trees with in every commit from the repo. It then processes this information and and read ready to give jobs to nodes requesting a job.<br />
The nodes are then given a file each from the "task_setter.py". The resutls are then returned to this file and stored in order to caculate the avarage CC (Code Complexity). <br />
When all the task (this being the CC caculated on each file) are completed the "task_setter.py" tells the nodes when they requesta new job. <br />
Finally the results are writen to a file called "Results.txt"

### node.py

This file is a worker that calls on the "task_setter.py" to do work. It gets a responce.<br />
It reseives the commit identifier "sha", the file name "path", and the status "status" this allows the node to pull the raw file contence form the githb API.<br />
It then caculates the code complexity of the given file using Radon. <br />
Finally the node returns the information to the "task_setter.py" and asks for anouther task.<br />

## Built With


* [Radon](http://radon.readthedocs.io/en/latest/api.html#module-radon.complexity) - Used to caculate CC
* [Flask](https://flask-restful.readthedocs.io/en/latest/) - Used to communicated between node and task setter
* [GitAPI](https://developer.github.com/v3/) - Used to get info from the git repos


