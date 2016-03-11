<!-- TOC depthFrom:1 depthTo:6 withLinks:1 updateOnSave:1 orderedList:0 -->

- [Project software site](#project-software-site)
- [Generate files](#generate-files)
	- [Config](#config)
	- [Repositories](#repositories)
	- [Publications](#publications)
- [Local hosting](#local-hosting)
- [Update website automatically](#update-website-automatically)

<!-- /TOC -->

TODO 
1. Replace akkurat font with 
@import url(https://fonts.googleapis.com/css?family=Open+Sans+Condensed:300);
font-family: 'Open Sans Condensed', sans-serif;


# Project software site

Website listing the software and other output used/made/changed in this NLeSC project.

# Generate files

Install requirements with:
```
pip install -r utils/requirements.txt
```

## Config

```
python utils/generate.py config <organization name>
```

This will use the Github API to fetch information about the organization and write the `_config.yml` file. The `_config.yml` must be edited to complete the configuration.

## Repositories

```
python utils/generate.py repos <organization name>
```

This will generate a Markdown file in `_repos` directory for each public repo found in the organization.

## Publications

The list of doi's in `_data/dois.yml` can be converted to a publication list `_includes/publications.html` by
```
python utils/generate.py publications
```

The default citation style is `apa`.

# News items

Creating news item can be done by creating a Markdown file in the `_posts` directory.

The files should be called `YEAR-MONTH-DAY-title.md` and contain the following front matter.
```
---
title: New version of software X
---
```

See https://jekyllrb.com/docs/posts/ for more information.

# Team members

The team members of the project can be displayed on this website.

To add a new member create a biography file in `_team_members/` directory where the filename should be the person name.
The following front matter should be used.
```
---
title: <Name of person>
photo: <Url of photo of person, eg. /assets/team_members/name_of_person.jpg>
role: <Role of person>
---
```
A photo of the person should be added to the `assets/team_members/` directory with the same name as the biography.

# Local hosting

```
docker run --rm --volume=$(pwd):/srv/jekyll -i -t  -p 127.0.0.1:4000:4000 jekyll/jekyll:pages
```

The website can be viewed at http://localhost:4000

# Update website automatically

This website can be automatically updated see [BUILD_NIGHTLY.md](BUILD_NIGHTLY.md) and [BUILD_ON_CHANGE.md](BUILD_ON_CHANGE.md).
