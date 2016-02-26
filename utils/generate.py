#!/usr/bin/env python

# Copyright 2016 Netherlands eScience Center
#
# Licensed under the Apache License, Version 2.0 (the 'License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import logging
from os import mkdir, sep
from string import Template

import github3
import yaml


def generate_config(organization, configfn):
    gh = github3.GitHub()
    org = gh.organization(organization)

    config = {
        'title': org.name,
        'slug': org.login,
        'description': org._json_data['description'],
        'baseurl': '',
        'created_at': org.created_at,
        'urls': {
          'avatar': org.avatar_url,
          'organization': org.html_url,
          'project': org.blog,
        },
        'partners': [{
            'logo_url': 'https://www.esciencecenter.nl/img/pressroom/ESCIENCE_logo_C_nl_cyanblack.jpg',
            'url': 'https://www.esciencecenter.nl'
        }, {
            'logo_url': '<FIXME AND OPTIONALLY REPEATME>',
            'url': '<FIXME AND OPTIONALLY REPEATME>'
        }],
        'markdown': 'kramdown',
        'excludes': [
            'README.md',
            'utils',
        ],
        'keep_files': [
            '<FIXME files directories Jekyll should not alter>'
        ],
        'collections': ['repos']
    }

    yaml.dump(config, configfn, default_flow_style=False)


def generate_repo(repo, repo_fn):
    repo_tpl = Template('''---
title: $title
language: $language
license: $license
homepage: $homepage
github: $github_url
---
$description
    ''')
    config = {
        'title': repo.name,
        'description': repo.description,
        'language': repo.language,
        'license': repo.license().license['name'],
        'homepage': repo.homepage or repo.html_url,
        'github_url': repo.html_url,
    }
    if not repo.homepage:
        logging.warning('{} has no homepage, falling back to github repo'.format(repo.name))
    repo = repo_tpl.substitute(config)

    with open(repo_fn, 'w') as repo_markdown_file:
        print(repo, file=repo_markdown_file)


def generate_repos(organization):
    gh = github3.GitHub()
    org = gh.organization(organization)

    repos_dir = '_repos'
    try:
        mkdir(repos_dir)
    except OSError:
        pass

    for repo in org.repositories('public'):
        if repo.name.endswith('github.io'):
            # skip self
            continue
        repo_fn = '{}/{}.md'.format(repos_dir, repo.name)
        generate_repo(repo, repo_fn)


def main():
    parser = argparse.ArgumentParser(description='Generate Jekyll files')
    subparsers = parser.add_subparsers()

    config_parser = subparsers.add_parser('config', help='Generate Jekyll _config.yml file')
    config_parser.add_argument('organization', help='Github organization or user name')
    config_parser.add_argument('configfn',
                               default='_config.yml',
                               type=argparse.FileType('w'),
                               help="Filename for config file. Default _config.yml. Use - for stdout")
    config_parser.set_defaults(func=generate_config)

    config_parser = subparsers.add_parser('repos', help='Generate markdown file for organization repos')
    config_parser.add_argument('organization', help='Github organization or user name')
    config_parser.set_defaults(func=generate_repos)

    args = parser.parse_args()
    fargs = vars(args)
    if 'func' in args:
        func = args.func
        del(fargs['func'])
        func(**fargs)

if __name__ == "__main__":
    main()
