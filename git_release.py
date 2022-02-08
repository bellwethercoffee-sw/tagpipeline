import fileinput
import os
import requests
import re
from git import Repo
import datetime
REPO_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', ''))


def get_latest_release(owner: str, repo_name: str) -> str:
    r = requests.get(
        url=f'https://api.github.com/repos/{owner}/{repo_name}/releases/latest')
    data = r.json()
    return data['tag_name']

#v1.0.1-beta-1+20220201.sha.2b9027f
def increment_ver(version,date,hash):
    version = version.split('-')
    beta_ver = version[2].split("+")
    version = version[0]+"-"+version[1]+"-"+beta_ver[0]+"+"+date+".sha."+hash
    return version

def replace_version_string(file_name: str, previous_version: str, next_version: str):
    print(f'{file_name} updated')
    with fileinput.FileInput(f'{REPO_PATH}/{file_name}', inplace=True) as file:
        for line in file:
            print(line.replace(previous_version, next_version), end='')

if __name__ == '__main__':
    date = datetime.datetime.now().strftime('%Y%m%d')
    print(date)
    repo = Repo('.', search_parent_directories=True)
    REPO_PATH = repo.working_tree_dir
    repo = Repo(REPO_PATH)
    # tags = sorted(repo.tags, key=lambda t: t.commit.committed_datetime)
    # latest_tag = str(tags[-1])
    latest_tag = "v1.0.1-beta-1+20220201.sha.2b9027f"
    print(latest_tag)
    commit = repo.git.commit('-am', f'Prepare for release {latest_tag}')
    new_commit_hash = commit.split('] ')[0].split(' ')[1]
    new_tag_version = increment_ver(str(latest_tag),date,new_commit_hash)
    print(new_tag_version)
    new_tag = repo.create_tag(new_tag_version, message=f'Version {new_tag_version}', ref=commit)
    repo.git.push('--set-upstream', 'origin')
    repo.remotes.origin.push(new_tag)
    # #REPLACE VERSION IN THE FILE
    # with open('README.md', 'r') as file:
    #     filedata = file.read()
    # filedata = filedata.replace(latest_tag, new_tag)
    # print(filedata)
    # with open('README.md', 'w') as file:
    #     file.write(filedata)
