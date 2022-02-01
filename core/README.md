# Core

The core contains common utilities needed across most services such as:
* mongoDB connection
* requests
* exception handlers

Core will already be installed as a dependency (via pipenv) on the services that need it.

---

#### Setup MongoDB user
```
# connect:
$ mongo

# create user calendar as a superuser:
mongo> use admin
mongo> db.createUser({
  user: "test",
  pwd: "test",
  roles: ["root"]
})
```

---
