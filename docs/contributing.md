Contributing
============

Firstly, thanks for helping me!

Below you'll find how to prepare you machine, run project locally and contribute to this project.


Preparing your environment
==========================

```bash
$ git clone git@github.com:filwaitman/dlogr-web.git
$ cd dlogr-web/
$ pip install -r requirements.txt
$ pip install -r requirements_test.txt
```


Running project
===============

`make serve` starts the server on port 8000.
`make shell` starts the django shell.
`make test` runs the test suite.


How to contribute
=================

* Please follow the PEP8 with 120 characters as max line length
  * If you don't do that `make test` this will fail, and so the CI.

* Make your changes compatible with both Python2 (at least 2.7) and Python3 (from 3.5 on)
  * If you don't do that the CI will fail.
