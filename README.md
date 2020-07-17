# Warehouse

## Installation

Clone remote repository.

```
git clone https://github.com/langoon/warehouse.git
```

Grant execution rights on the init file.

```
chmod +x ./scripts/init
```

Initialize the workspace by running this script.

```
sudo ./scripts/init
```

It should clone the repo, install all dependencies and start a webserver running on port `8080`.

If the webserver needs to be restarted, then use this script:

```
node scripts/webserver.js
```

## Usage

This repo follows a [GitHub Flow](https://guides.github.com/introduction/flow/) branching strategy, whereas all new features are branched out of the `master` branch into a named `feature` branch, this branch is committed to regularly and when the work is done a push is made and a pull request created to merge with master.

### Workflow

#### 1. Create a feature branch

Before working on a new feature make sure the most recent changes on the codebase is fetched from master.

```
git pull origin master
```

Then checkout to a new feature branch. Make sure the name is descriptive and concise, i.e.

```
git checkout updating-readme-installation-instructions
```

Finally publish the branch to the remote repo.

```
git push -u origin updating-readme-installation-instructions
```

#### 2. Commit new changes

Commit new code regulary with descriptive headers, for example:

```
git commit -m "Changed the workflow instructions to correspond with new branching strategy"
```

Also make sure it is pushed to the remove repo:

```
git push -u origin updating-readme-installation-instructions
```

#### 3. Merge 

When it is time to merge the code with master, you need to make sure that there are no merge conflicts. You do that by pulling in the most recent state of the code base.

```
git pull origin master
```

If there are merge conflicts these needs to be resolved and then pulled back into the remote repo.

```
git push -u origin updating-readme-installation-instructions
```

Once ready to be merge, head over to [GitHub](https://github.com), select the branch you are working on and create a **Pull Request**. If you want your code to be reviewed prior to merging then add a reviewer to the pull request.

Complete the pull request and your feature will now be deployed to the remote repo.

#### 4. Deploy

A successfull merge with master will be automatically deployed to the device if set up properly in GitHub Webhooks.