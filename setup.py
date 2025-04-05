from setuptools import setup, find_packages

setup(
    name="GroupMinPrereq",
    version="1.0",
    packages=find_packages(),
    entry_points={
        "cms.grading.scoretypes": [
            "GroupMinPrereq=scoretypes.GroupMinPrereq:GroupMinPrereq"
        ]
    }
)
