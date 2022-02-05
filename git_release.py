import fileinput
import os
import requests
import re
from git import Repo
import datetime

def increment_ver(version):
    version = version.split('.')
    version[2] = str(int(version[2]) + 1)
    return '.'.join(version)

if __name__ == '__main__':
    now = datetime.datetime.now().strftime('%Y-%m-%d')
    print(now)
    repo = Repo('.', search_parent_directories=True)
    REPO_PATH = repo.working_tree_dir
    repo = Repo(REPO_PATH)
    tags = sorted(repo.tags, key=lambda t: t.commit.committed_datetime)
    latest_tag = str(tags[-1])
    print(latest_tag)
    new_tag = increment_ver(str(latest_tag))
    #new_tag_date = new_tag+"-"+str(now)
    new_tag_date = new_tag
    print(new_tag_date)
    #REPLACE VERSION IN THE FILE
    with open('README.md', 'r') as file:
        filedata = file.read()
    filedata = filedata.replace(latest_tag, new_tag_date)
    print(filedata)
    with open('README.md', 'w') as file:
        file.write(filedata)
    repo.git.commit('-am', f'Prepare for release {new_tag_date}')
    new_tag = repo.create_tag(new_tag_date, message=f'Version {new_tag_date}')
    repo.git.push('--set-upstream', 'origin')
    repo.remotes.origin.push(new_tag_date)
