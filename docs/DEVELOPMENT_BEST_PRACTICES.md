# Best Practices

## Git

This project uses [GitHub Flow](https://guides.github.com/introduction/flow/) and follows a couple
of simple principles:

* All code on the `main` branch is in production.
* All code going into `main` must go through a pull request.
* All pull requests must pass GitHub Action checks and have multiple reviewers.
* To deploy code into environments other than production git tags are used. IE: `STAGING`, `BETA`

### Commit messages

Commit messages are very important. They tell other developers what you did without them having to
read all the changes you made. Commit messages should be in the form:

```text
#<GitHub issue number>: <Description of what you did>
```

IE:

```text
#15: Added endpoints for adding/removing users,
added constants to consts.py,
added user schema.
```

### Branches

#### Main

Code on the main branch is in production. All code merged into main must go through a PR.

#### Feature

Feature branches are the catch-all branches. If you are not fixing a bug or doing a hotfix then it
should be on a feature branch.

These branches must be deployed to STAGING and tested before being released.

Feature branches naming convention are as
follows: `feature/<github ticket_number>_<short_description>` IE: `feature/#15_example_ticket`

#### Bugfix

Bugfix branches are used when working a ticket labeled as a bug. Bugfixes differ from hotfixes in
hotfixes are an issue that is causing production to fail. Bugfixes can take longer and are not a
drop everything to resolve issue.

These branches must be deployed to STAGING and tested before being released.

Bugfix branches naming convention are as
follows: `bugfix/<github ticket_number>_<short_description>` IE: `bugfix/#2_example_bugfix_ticket`

#### Hotfix

Hotfix branches are ONLY used when there is a production issue that has to be resolved ASAP.

Hotfix branches are the only branches that can be deployed directly into production without being
deployed to a test environment first. All other branches must be deployed to the staging environment
prior to being merged to `main`

Feature branches naming convention are as
follows: `hotfix/<github ticket_number>_<short_description>` IE: `hotfix/#1_stop_everything_and_fix`

### Merging

All merging must be done via a pull request. All pull requests must pass the GitHub actions.

All merges to `main` must have been deployed to staging and tested. Except for hotfix branches.

## Editors

This project provides a .editorconfig file that tells your editor how to treat some files. This
includes 4 spaces per tab in python files, no whitespace at the end of lines, and using lf as the
new line character.

Pycharm and VSCode are the officially supported editors, but almost any editor will work. Including
vim.

## Linters and formatters.

This project uses the [isort](https://pycqa.github.io/isort/)
, [black formatter](https://black.readthedocs.io/en/stable/),
and [Flake8](https://flake8.pycqa.org/en/latest/) to ensure everyone's code follows the same
standards and best practices. The code standards are enforced on commit time via pre-commit, and
during pull requests via GitHub actions.

These tools can be run outside of commit by running `make check` in your terminal. NOTE: Running
this can change your files.

Black will automatically reformat your files, and isort will reorder your imports. This will never
break your code, just change how it looks.

Flake8 will check some python best practices and throw error messages if you have any.

## Static analysis

[Mypy](http://mypy-lang.org/) runs a some static analysis on python types to help avoid some common
errors. Mypy can be run using `make check` or on its own `mypy tests/ src/`.
