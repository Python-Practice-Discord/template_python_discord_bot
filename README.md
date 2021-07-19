<p align="center">
    <a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
</p>

# Using this template

The projects' name should be `lower_snake_case`. This should be the same name as the projects' root
directory.

* Find all instances of `replaceme` or `project name` and replace them with the project's name in
  these locations:
    * Change the name of `./src/project_template` to `./src/<project_name>`
    * README.md
* Change Github settings for the new repo:
    * Protect the main and staging branches with both actions.
    * Require pull request reviews before merging
        * require review from code owner
    * Require conversation resolution before merging
    * Require branches to be up to date before merging
    * Configure repository access:
        * Base access level for organization members should be `Read`
        * Group Project Team Leads should have `Maintain` permissions
        * The Project Team should have `Write` permissions
* Add project description in README.md
* Add usage instructions in README.md
* Run through [Sentry Init](docs/SENTRY.md#init)
* Run through [Heroku Init](docs/cloud_providers/HEROKU.md#init)

# Project Name

This project is run by the [Python Practice](https://discord.gg/Zp8CBHvudz) Discord community.

**Brief Project Description Here**

# How to use this project as a non contributor

Add usage and/or installation instructions here, as stated in "Using this Template"

# Documentation

To view all the available documentation for this project please see
our [Documents Index](/docs/INDEX.md). This includes how to get started, our coding best practices,
and more.
