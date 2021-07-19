# Init

* Go to [Heroku](https://www.heroku.com/) and create an account (if you don't already have one)
* Create a new app
* Name the app
* Select GitHub under `Deployment Method`
* Select this git repo
* Type in `main` under `Enter the name of the branch to deploy`
* Check the `Wait for CI to pass before deploy`
* Select `Enable Automatic Deploys`
* Install the Heroku CLI tool from [here](https://devcenter.heroku.com/articles/heroku-cli)
* In your terminal run `heroku stack:set container -a <name of heroku app>`
* If you want to deploy your current code press `Deploy Branch` in the `Manual deploy` section
* Wait for the docker container to build and release (This might take 5+ minutes)
* Go to the `Resources tab`
* There should be an entry under `Free Dynos`. Click the `Edit` button
* Click the slider button to make it blue (if it is not already blue).
* Press confirm.

Your project is now deployed on heroku for free!

# Deployment

If you followed the setups in Init then every push to the `main` branch of your GitHub repo should
automatically deploy your code.


# Secrets
* In your app go to `Settings`
* Click `Reveal Config Vars`
* Add your secret keys and values here.
