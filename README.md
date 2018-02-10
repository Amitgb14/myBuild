# mybuild


Setup master
-------------
```
$ mkdir -p ~/tmp/bb-master
$ cd ~/tmp/bb-master
```
```
$ virtualenv --no-site-packages sandbox
$ source sandbox/bin/activate
```

* Install buildbot
```
$ pip install --upgrade pip
$ pip install 'buildbot[bundle]'
```
```
$ buildbot create-master master
$ mv master/master.cfg.sample master/master.cfg
```

* Start the master
```
$ buildbot start master
```

Setup worker
------------
```
$ mkdir -p ~/tmp/bb-worker
$ cd ~/tmp/bb-worker
```
```
$ virtualenv --no-site-packages sandbox
$ source sandbox/bin/activate
```

* Install buildbot-worker
```
$ pip install --upgrade pip
$ pip install buildbot-worker
# required for `runtests` build
$ pip install setuptools-trial
```

* Create the worker
```
$ buildbot-worker create-worker worker <worker-node> <worker-user> <pass>
```
* Start worker
```
$ buildbot-worker start worker
```



Buildbot master repo
--------------------

* LLVM

