
## Contributing

First off, thank you for considering contributing to **Cloud Instance Manager**. It's people like you that will make Cloud Instance Manager such a great solution.

### Where do I go from here?

If you've noticed a bug or have a feature request, [make one](https://github.com/emumba-com/cloud-instance-manager/issues/new)! It's generally best if you get confirmation of your bug or approval for your feature request this way before starting to code.
If you have a general question about cloud instance manager, you can email us at 
`cloud-instance-manager@gmail.com`

### Fork Cloud Instance Manager repository

If there is something you think you can fix, then fork [[how to](https://docs.github.com/en/free-pro-team@latest/github/getting-started-with-github/fork-a-repo#)] [Cloud Instance Manager](https://github.com/emumba-com/cloud-instance-manager) and create a branch with a descriptive name. 
A good branch name would be (where issue #111 is the ticket you're working on):
```
git checkout -b 111-add-system-help
```
### Get the Cloud Instance Manager running

Make sure, you've followed instructions from [README.md](https://github.com/emumba-com/cloud-instance-manager#cloud-instance-manager) file to install and set up the project to run it fine locally.

### Implement your fix or feature

At this point, you're ready to make your changes! Feel free to ask for help; everyone is a beginner at first :smile_cat:

### View your changes locally

After implementing a bugfix/feature, make sure to take a look at your changes in a browser.  Follow the instructions to [run application locally](https://github.com/emumba-com/cloud-instance-manager#iii-running-application-locally).

You should now be able to open <http://localhost:5000/> in your browser and log in with your username and password.

### Get the coding style right

Your patch should follow the same conventions & pass the same code quality checks as the rest of the project. 
Run the following commands to ensure code quality is up to the mark.
 ```
 pycodestyle --config=setup.cfg
 pylint models/*.py
 pylint server/*.py
 pylint *.py
 ```
 
### Make a Pull Request

At this point, you should switch back to your `main` branch and make sure it's up to date with Cloud Instance Manager's `main` branch:

```sh
git remote add upstream https://github.com/emumba-com/cloud-instance-manager.git
git checkout main
git pull upstream main
```

Then update your feature branch from your local copy of main, and push it!

```sh
git checkout 111-add-system-help
git merge upstream/main
git push --set-upstream origin 111-add-system-help
```

Finally, go to GitHub and make a [Pull Request](https://docs.github.com/en/free-pro-team@latest/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request). CICD pipeline will run to make sure build and test jobs are passed. 

### Keep your fork synced
To have code updated on your repository, make sure to keep sync your repo with the upstream repository.
Follow [this](https://docs.github.com/en/free-pro-team@latest/github/collaborating-with-issues-and-pull-requests/syncing-a-fork) link to keep code updated. 


### Keeping your Pull Request updated

If a maintainer asks you to "rebase" your PR, actually, they're saying that a lot of code has changed and that you need to update your branch so it's easier to merge.

To learn more about rebasing in Git, there are a lot of [good](http://git-scm.com/book/en/Git-Branching-Rebasing)  [resources](https://help.github.com/en/github/using-git/about-git-rebase) but here's the suggested workflow:

```sh
git checkout 111-add-system-help
git pull --rebase upstream main
git push --force-with-lease 111-add-system-help
```

### Merging a PR (maintainers only)

A PR can only be merged into main by a maintainer if:

* It is passing CI.
* It has been approved by at least one maintainer. 
* It is up to date with the current main.

If all of these above conditions are met, the maintainer will merge PR.