# Core

The core contains common utilities needed across most services such as:
* mongoDB connection
* requests
* exception handlers

Core will already be installed as a dependency (via pipenv) on the services that need it.

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
  user: "test",
  pwd: "test",
  roles: ["root"]
})

# stop:
brew services stop mongodb-community
# restart:
brew services restart mongodb-community
```

---
