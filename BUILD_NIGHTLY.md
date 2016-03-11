<!-- TOC depthFrom:1 depthTo:6 withLinks:1 updateOnSave:1 orderedList:0 -->

- [Nightly update setup](#nightly-update-setup)
	- [Setup Travis-CI](#setup-travis-ci)
	- [Github deploy key to allow Travis-CI to git push](#github-deploy-key-to-allow-travis-ci-to-git-push)
		- [Add deploy key to Github](#add-deploy-key-to-github)
		- [Add encrypted deploy key to repo](#add-encrypted-deploy-key-to-repo)
	- [Manually trigger a build](#manually-trigger-a-build)
	- [Register repo on https://nightli.es/](#register-repo-on-httpsnightlies)

<!-- /TOC -->

# Nightly update setup

Inspiration for the website is http://twitter.github.io/ or http://hadley.github.io/.
Problem with those websites is they use the Github API anonymously.  Which is limited to 60 requests an hour.

A solution to this is to perform nightly builds of organization website.

1. https://nightli.es/ will trigger travis-ci builds.
2. The build will fetch stats using Github API and write/commit/push the results as a json file.
3. Github Pages will host this new json file.
4. Site visitors will see stats of at most a day old.

An alternative solution which monitors all organization repos for changes to trigger a build is documented in [BUILD_ON_CHANGE.md](BUILD_ON_CHANGE.md).

## Setup Travis-CI

1. Goto `https://travis-ci.org/profile/<project name>`.
2. Activate Travis-CI for `<project name>.github.io` repo.
3. Goto settings of `<project name>.github.io` repo.
4. Turn off `Build pushes`
5. Turn off `Build pull requests`

The build will only be triggered by nightli.es.

## Github deploy key to allow Travis-CI to git push

To commit and push in Travis-CI we need a key pair.

The public key needs to be registered in the Github settings and the encrypted private key needs to added to the repo.

Generate a ssh key pair with

```
ssh-keygen -t rsa -f travis-ci.key -P '' -C '<organization name>@travis-ci.org'
```

This will generate
* travis-ci.key.pub, use as Github deploy key
* travis-ci.key, use in Travis-CI job

### Add deploy key to Github

Add deploy key to Github repo containing the organization pages.

1. Goto `https://github.com/<organization name>/<organization name>.github.io/settings/keys`
2. Add deploy key

  * Title = Travis-CI build
  * Key = `<content of travis-ci.key.pub>`
  * Check Allow write access

3. Press `Add key` button

### Add encrypted deploy key to repo

Use travis cli to encrypt `travis-ci.key` file.

0. Use travis cli from docker container
```
alias travis='docker run -it --rm -u $UID -v $PWD:/data -e TRAVIS_CONFIG_PATH=/data/.travis jamespamplin/alpine-travis-cli'
```
1. Login with Github credentials
```
travis login
```
2. Encrypt key
```
travis encrypt-file travis-ci.key
```
3. Add printed openssl command to .travis.yml in before_install stage
4. Add `travis-ci.key.enc` file to repo
5. Commit changes.
6. Push changes.

## Manually trigger a build

Use the Travis-CI API to trigger a build (https://docs.travis-ci.com/user/triggering-builds).
To Travis-CI API requires a token.

Token can be fetched using
```
travis token
```

Trigger build with
```
curl -s -X POST \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -H "Travis-API-Version: 3" \
  -H "Authorization: token <travis-ci token>" \
  -d "{ \"request\": { \"branch\": \"master\"}}" \
  https://api.travis-ci.org/repo/<organization>%2F<organization name>.github.io/requests
```

## Register repo on https://nightli.es/

1. Goto https://nightli.es/
2. Login
3. On dashboard turn this repo ON

Now every night a Travis-CI build will be triggered which will update the stats.json file.
