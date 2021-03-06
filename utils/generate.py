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

from __future__ import print_function
import argparse
from datetime import datetime
import logging
from os import mkdir
from os.path import isfile
from string import Template
import urllib2

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
            'assets',
            '<FIXME files directories Jekyll should not alter>'
        ],
        'collections': {
            'repos': {
                'output': False
            },
            'team_members': {
                'output': True,
                'permalink': '/team/:path'
            }
        },
        'defaults': [{
            'scope': {
                'path': '',
                'type': 'posts'
            },
            'values': {
                'layout': 'post'
            },
            'scope': {
                'path': '',
                'type': 'team_members'
            },
            'values': {
                'layout': 'team'
            }
        }]
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
        if isfile(repo_fn):
            # Don't overwrite
            continue
        generate_repo(repo, repo_fn)


def generate_publication(doi, style):
    logging.warn('Fetching meta data for {}'.format(repr(doi)))
    url = 'http://dx.doi.org/' + doi
    opener = urllib2.build_opener()
    opener.addheaders = [('Accept', 'text/bibliography; style={}'.format(style))]
    try:
        response = opener.open(url)

        publication = response.read()
        publication_html = '<li>{}</li>'.format(publication)
        if doi in publication_html:
            if url in publication_html:
                publication_html = publication_html.replace(url, '<a href="{}">{}</a>'.format(url, url))
            else:
                publication_html = publication_html.replace(doi, '<a href="{}">{}</a>'.format(url, doi))
        return publication_html
    except urllib2.HTTPError:
        logging.warn('Unable to fetch publication for {}, skipping'.format(doi))
        return ''


def generate_publications(style, dois_fn, publications_fn):
    dois = yaml.load(dois_fn)

    header = '''<!-- This files has been generated by `python utils/generate.py publications` on {now} -->
<h2><a name="publications"></a><span class="mega-octicon octicon-book"></span>&nbsp;Publications</h2>
<ul>
    '''.format(now=datetime.now())

    print(header, file=publications_fn)

    if dois is not None:
        for doi in dois:
            publication = generate_publication(doi, style)
            print(publication, file=publications_fn)

    print('</ul>', file=publications_fn)


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

    repos_parser = subparsers.add_parser('repos', help='Generate markdown file for organization repos')
    repos_parser.add_argument('organization', help='Github organization or user name')
    repos_parser.set_defaults(func=generate_repos)

    publ_parser = subparsers.add_parser('publications', help='Generates publications html file')
    publ_parser.add_argument('dois_fn',
                             type=argparse.FileType('r'),
                             default='_data/dois.yml',
                             nargs='?',
                             help='Filename of dois yaml file')
    publ_parser.add_argument('publications_fn',
                             type=argparse.FileType('w'),
                             default='_includes/publications.html',
                             nargs='?',
                             help='Filename of publications html file')
    publ_parser.add_argument('--style',
                             default='apa',
                             help='Style of citation, see http://api.crossref.org/styles for supported styles, default is apa')
    publ_parser.set_defaults(func=generate_publications)

    args = parser.parse_args()
    fargs = vars(args)
    if 'func' in args:
        func = args.func
        del(fargs['func'])
        func(**fargs)

if __name__ == "__main__":
    main()
