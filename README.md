# Warehouse

## Installation

### Clone remote repository

Login to Raspberry P, clone the remote repository and `cd` in to the working directory.

```
git clone https://github.com/langoon/warehouse.git
cd warehouse
```

### Initialize the workspace

Grant execution rights and execute the script using admin privileges.

If you are initalizing the workspace on a Raspberry Pi then a DEVICE_TOKEN has to be specified. The device token is used bu clients for making authenticated requests to the web server. It cannot be empty.

```
chmod +x ./scripts/install-binaries.sh ./scripts/install-dependencies.sh ./scripts/start-services.sh ./scripts/initialize.sh
./scripts/initialize.sh --token <token> --ci <true|false>
```

This should upgrade all the binaries, start a running instance of VNC Server, install all the project dependencies and start a webserver running on port `8080`.

### Starting services

Sometimes you might need to reboot the services on the workspace. You can do that running this script.

If you are initalizing the workspace on a Raspberry Pi then a DEVICE_TOKEN has to be specified.

```
chmod +x ./scripts/start-services.sh
./scripts/start-services.sh  --token <token> --ci <true|false>
```

## Usage

### Tests

To run all unit tests, run this command:

```
python3 -m unittest
```

### Workflow

This repo follows a [GitHub Flow](https://guides.github.com/introduction/flow/) branching strategy, whereas all new features are branched out of the `master` branch into a named `feature` branch, this branch is committed to regularly and when the work is done a push is made and a pull request created to merge with master.

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

## Troubleshooting

### Can't install `picamera`

When installing this module on a device other than Raspberry Pi it own't work. To fix this you better install it directly from GitHub to use the classes and methods:

```
pip3 install git+https://github.com/waveform80/picamera.git
```
