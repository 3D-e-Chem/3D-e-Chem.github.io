# Project software site

Website listing the software used/made/changed in this NLeSC project.

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

# Local hosting

```
docker run --rm --volume=$(pwd):/srv/jekyll -i -t  -p 127.0.0.1:4000:4000 jekyll/jekyll:pages
```


# Automatic update setup

Inspiration for the website is http://twitter.github.io/ or http://hadley.github.io/.
Problem with those websites is they use the Github API anonymously.  Which is limited to 60 requests an hour.

Solution to this is:

1. Use Github webhooks in repositories to trigger when something changes.
2. Webhook urls are listened on a IFTT recipe using it's Maker channel (https://github.com/captn3m0/ifttt-webhook)
3. The IFTT recipy triggers a Travis-CI build (https://docs.travis-ci.com/user/triggering-builds)
4. The Travis-CI build will fetch data using Github API and write/commit/push the results as a json file.
5. Github Pages will host this new json file.
6. Site visitors will see up 2 date data.

## Setup IFFTTT Maker endpoint

1. Login to https://ifttt.com/
2. Goto https://ifttt.com/maker
3. Click on `How to Trigger Events`
4. Replace `{event}` by organization name.
5. Store the url for later

The url will be `https://maker.ifttt.com/trigger/<organization name>/with/key/<IFTTT Maker key>`

## Setup Github webhooks

Foreach repository in the Github Organization create a webhook in the repo settings.

* Payload URL = IFFTTT Maker endpoint
* Which events would you like to trigger this webhook? = Let me select individual events.
* Select the following events
  * Push
  * Issues
  * Fork
  * Watch
  * Release

## Github key for Travis-CI

To commit and push in Travis-CI we need a .

0. Generate a ssh key pair

```
ssh-keygen -t rsa -f travis-ci.key -P '' -C '<organization name>@travis-ci'
```

This will generate
* travis-ci.key.pub, use as Github deploy key
* travis-ci.key, use in Travis-CI job

1. Goto `https://github.com/<organization name>/<organization name>.github.io/settings/keys`
2. Add deploy key

  * Title = Travis-CI json update
  * Key = `<content of travis-ci.key.pub>`
  * Check Allow write access

3. Press `Add key` button

## Setup Travis-CI

1. Goto `https://travis-ci.org/profile/<project name>`.
2. Activate Travis-CI for `<project name>.github.io` repo.
3. Goto settings of `<project name>.github.io` repo.
4. Turn off `Build pushes`
5. Turn off `Build pull requests`
6. Add Github deploy key to environment variable.
  * Key = DEPLOY_KEY
  * Value = `<content of travis-ci.key>`
  * Display value = turned off

To trigger a build a Travis-CI token is required.
This can be found on https://travis-ci.org/profile/ page.
Click on the eye icon next to 'Token' to get your token.

## Listen for Github webhook using IFTTT recipe and trigger Travis-CI build

Goto https://ifttt.com/myrecipes/personal/new

0. Select 'this'
1. Filter on 'Maker'
2. Select 'Maker' channel
2. Select 'Receive a web request'
4. Set Event Name = organization name (eg. 3D-e-Chem)
5. Select 'that'
6. Filter on 'Maker'
7. Select 'Maker' channel
8. Select 'Make a web request'

  * URL =  https://api.travis-ci.org/repo/<organization name>%2F<organization name>.github.io/requests (eg. https://api.travis-ci.org/repositories/3D-e-Chem%2f3D-e-Chem.github.io/requests)
  * Method = POST
  * Content Type = application/json
  * Body =

```
{
  "request": {
    "branch": "master",
    "token": "<Travis-CI token>"
  }
}
```  

9. Recipe title = Trigger Travis-CI build of <organization name>.github.io Github repo on any <organization name> repo change.
10. Disable `Recieve notifiactions`
11. Press `Create recipe` button
