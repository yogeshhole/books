# Calendar Core

The calendar core contains common utilities needed across most services such as:
* user JWT auth
* mongoDB connection
* requests
* exception handlers
* date functions

Calendar core will already be installed as a dependency (via pipenv) on the services that need it.

(REQUIRED) setup SSH keys locally:
```
1 generate an SSH key pair (will add v2_calendar to ~/.ssh):
    ssh-keygen -t rsa -b 4096 -m PEM -P "" -f ~/.ssh/v2_calendar.key -C "system@calendar.com"

2 Add to your shell startup script (.bashrc or .zshrc):
    export CALENDAR_AUTH_PRIVATE_KEY=$(cat ~/.ssh/v2_calendar.key)
    export CALENDAR_AUTH_PUBLIC_KEY=$(cat ~/.ssh/v2_calendar.key.pub)

3 You will likely need to restart your IDE (pycharm, vscode) pick up the updated env changes
```
---

(OPTIONAL) Attach v2-calendar-core in Pycharm:
1. open a service
1. open v2-calendor-core and select `attach`

---

#### Install MongoDB 4.2 on OSX
```
reference: https://docs.mongodb.com/manual/tutorial/install-mongodb-on-os-x/#install-mongodb-community-edition

$ brew tap mongodb/brew
$ brew install mongodb-community@4.2
    # binaries: /usr/local/Cellar/mongodb-community
    # data: /usr/local/var/mongodb (for catalina, otherwise /data/db)

# To run MongoDB (i.e. the mongod process) as a macOS service
$ brew services start mongodb-community@4.2
$ brew services list≤

# verify MongoDB is running:
$ ps aux | grep -v grep | grep mongod
$ ps -ef | grep mongo

# connect:
$ mongo

# create user calendar as a superuser:
mongo> use admin
mongo> db.createUser({
  user: "calendar",
  pwd: "calendar",
  roles: ["root"]
})

# stop:
brew services stop mongodb-community
# restart:
brew services restart mongodb-community
```

---

#### pipenv quickstart:
https://dev.to/smirza/quickstart-guide-on-pipenv-python-packaging-tool-2ie4
