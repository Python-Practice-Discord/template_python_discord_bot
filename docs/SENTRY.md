

# Init

* Create a sentry.io account [here](https://sentry.io/signup/).
    * TIP: You can append words to the end of your email address to keep it organized by simply
      placing a `+` after your normal email and before the `@`.
      `<first>.<last>+cicd.project.template@gmail.com`
* Click `I'm Ready`
* Select `Python`
* Click `Create Project`
* Copy the value in the code example after the line `sentry_sdk.init(`. It is a URL starting with
  `https://`. This value is SECRET! DO NOT PUT IN REPO! See [the secrets doc](SECRETS.md) for
  more information on dealing with secrets.
    * You can click `View full documentation` for more info
* Add the copied secret to `.env` (create the `.env` file if it does not exist) under
`SENTRY_URL_ENV="https://<copied value>`
* Run `make run` in your terminal. You should see a `KeyError` raised from `main()`
* Back on the sentry website the `Take me to my error` button should not be clickable. Click it.
* Continue through the Sentry tutorial.


