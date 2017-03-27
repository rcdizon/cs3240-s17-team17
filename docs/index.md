# Lokahi Project Documentation
This page will be updated periodically on the standards the team will adopt for the project.
## GitHub Conventions
Before making any changes to the repo make sure that you do the following things:
* Pull down the most recent changes by doing the following Git commands
```
git checkout master
git pull
```

* If everything goes well and there isn't any weird activity, then your master branch has successfully been updated! Otherwise, post in the Slack chat for `#github` and we'll try to assist you with whatever problem you have.
* Now that your master branch has been updated, you're going to want to create a 'branch'. The naming convention will be `f_featureName` or `c_choreName` depending on whatever change you're making to the repo.
* To create a branch, do this and substitute `b_branchName` with the thing from the previous bullet:
```
git checkout -b "b_branchName"
```
* From here, it's safe to make changes within the branch!
* Once you've finished your task, do command `git status` to ensure that your changes to individual files have been recognized by Git. (They'll be highlighted in red)
* If everything is good, `git add .` will add the files for you. Do another `git status` to ensure all the necessary files have been added.
* After that, we're going to want to commit then push your changes with the following commands:
```
git commit -m "Message describing what you had to do
git push origin b_branchName
```
* Again, if all is good, then your branch was successfully uploaded to Git!

<!--- TODO: Add how to do code reviews and do code squash-merge, and pulldowns from the remote --->
