# cmsGroupMinPrereq
GroupMin with Prerequisite Grading for CMS.

## Prerequisites for installing
You must have a virtual environment of CMS, which is at, for example ~/cms_venv/ (you may replace this with your own directory). This is the virtual environment where CMS is installed and where you run CMS from. 

## Installation
```bash
# Clone repo
git clone https://github.com/Marszpace/cmsGroupMinPrereq.git

# Install the package
cd cmsGroupMinPrereq
~/cms_venv/bin/python3 setup.py install
# Alternatively, you may also use
source ~/cms_venv/bin/activate
python3 setup.py install
```
After this, restart CMS for it to pick-up to the task type

## Usage
The task type uses the parameter of the form `[true/false, [m, t, [p1, p2, ..., pi]], ... ]`, where `m` and `t` are multiplier and number of testcases in the subtask (functions like GroupMin). `p1...pi` are the prerequisites of the subtask. The first boolean argument is whether to show the results of prerequisites in a subtask or not. 
It is important that the prerequisites are only from the subtasks **before** the current one. 
Prerequisites of prerequisites can be handled by this score type too. (i.e. if 1 is prerequisite of 2, and 2 is prerequisite of 3, then 1 is automatically a prerequisite of 3 without the need for an additional parameter.
