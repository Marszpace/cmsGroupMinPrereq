# cmsGroupMinPrereq
GroupMin with Prerequisite Grading for CMS.

## Prerequisites for installing
1. The path of CMS must be available in the global scope, i.e. you must be able to import cms from anywhere. You may achieve this by installing CMS in the system 
2. You must have a virtual environment of CMS, which is at, for example ~/cms_venv/ (you may replace this with your own directory)

## Installation
```bash
# Clone repo
git clone https://github.com/Marszpace/cmsGroupMinPrereq.git

# Install the package
cd cmsGroupMinPrereq
~/cms_venv/bin/python3 setup.py install # or you may also activate then install. be careful if you use sudo
```
After this, restart CMS for it to pick-up to the task type

## Usage
The task type uses the parameter of the form `[[m, t, [p1, p2, ..., pi]], ... ]`, where `m` and `t` are multiplier and number of testcases in the subtask (functions like GroupMin). `p1...pi` are the prerequisites of the subtask. 
It is important that the prerequisites are only from the subtasks **before** the current one. 
Prerequisites of prerequisites can be handled by this score type too. (i.e. if 1 is prerequisite of 2, and 2 is prerequisite of 3, then 1 is automatically a prerequisite of 3 without the need for an additional parameter.
