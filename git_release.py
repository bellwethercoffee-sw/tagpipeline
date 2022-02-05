import fileinput
import os
import requests
from git import Repo
from datetime import datetime
REPO_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', ''))


def get_latest_release(owner: str, repo_name: str) -> str:
    r = requests.get(
        url=f'https://api.github.com/repos/{owner}/{repo_name}/releases/latest')
    data = r.json()
    return data['tag_name']


def create_release(previous_version: str, next_version: str):
    repo = Repo(REPO_PATH)
    # Create & checkout new release branch
    release_branch = repo.create_head(f'RELEASE-{next_version}')
    release_branch.checkout()
    # Update version in README.md
    replace_version_string('README.md', previous_version, next_version[1:])
    # Commit changes
    repo.git.commit('-am', f'Prepare for release {next_version[1:]}.')
    # Remove 'v' prefix and create tag
    new_tag = repo.create_tag(
        next_version[1:], message=f'Version {next_version[1:]}')
    # Push updates
    repo.git.push('--set-upstream', 'origin', release_branch)
    repo.remotes.origin.push(new_tag)


def replace_version_string(file_name: str, previous_version: str, next_version: str):
    print(f'{file_name} updated')
    with fileinput.FileInput(f'{REPO_PATH}/{file_name}', inplace=True) as file:
        for line in file:
            print(line.replace(previous_version, next_version), end='')


if __name__ == '__main__':
    latest_action_release = get_latest_release(
        owner='bellwethercoffee-sw', repo_name='tagpipeline')

    latest_action_version = f'v{latest_action_release}'

    create_release(latest_action_release, "test")
    print('new release')