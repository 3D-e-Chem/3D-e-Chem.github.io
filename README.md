<!-- TOC depthFrom:1 depthTo:6 withLinks:1 updateOnSave:1 orderedList:0 -->

- [Project software site](#project-software-site)
- [Generate files](#generate-files)
	- [Config](#config)
	- [Repositories](#repositories)
	- [Publications](#publications)
- [Local hosting](#local-hosting)
- [Update website automatically](#update-website-automatically)

<!-- /TOC -->

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

# Local hosting

```
docker run --rm --volume=$(pwd):/srv/jekyll -i -t  -p 127.0.0.1:4000:4000 jekyll/jekyll:pages
```

# Update website automatically

This website can be automatically updated see [BUILD_NIGHTLY.md](BUILD_NIGHTLY.md) and [BUILD_ON_CHANGE.md](BUILD_ON_CHANGE.md).
