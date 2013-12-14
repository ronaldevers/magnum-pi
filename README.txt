magnum-pi
=========

Meet magnum-pi, the very fast and dead-simple python package index
generator. It generates html index files from a directory of python
packages which you then serve as static files using your webserver of
choice. You can then install packages from your own index, independent
of PyPI, using standard python tools such as setuptools and pip.

Magnum-pi started out as a fork of basketweaver. Contrary to
basketweaver, magnum-pi never extracts anything from a package and
instead only inspects filenames. Because of this change magnum-pi runs
typically take only a fraction of a second. Besides the speed gains
the other major changes are support for Python 3.3 and wheel packages.

The only code left from basketweaver is the html output loop. Credit
for that goes to its authors Christopher Perkins and Chris McDonough.


# Installing

Get it from pypi:

    pip install magnum-pi


# Using

The basic workflow is

1. upload a new package to your packages directory
2. run magnum-pi on that directory
3. serve the packages and generated html files using a web server

So after you add a new package file, let's say you put it at
/var/www/magnum-pi, you run magnum-pi like so:

    makeindex /var/www/magnum-pi

This generates the top-level and per-project index.html files needed
by python installation tools. The index is always generated inside the
packages directory. It should run very fast. In my case, 0.073 seconds
for 385 packages.

Next you should serve the entire packages directory of packages and
index files with a web server.


# Serve using nginx

Add a site config like this:

    server {
      server_name magnum-pi.dev;
      root /var/www/magnum-pi;
      index index.html;
      autoindex on;
    }


# Installing packages from your own index

After you setup your own index using the instructions outlined above,
you are now ready to install packages from it. For pip you will need a
version recent enough that it support the --index-url option.

    pip install --use-wheel --download-cache ~/.cache/pip --index-url http://magnum-pi.dev/index <package>
    pip install --use-wheel --download-cache ~/.cache/pip --index-url https://magnum-pi.dev/index --cert ca.crt <package>
    easy_install --index-url http://magnum-pi.dev/index <package>

Don't miss the `/index` at the end of the index url or it won't work!


# Changes

## 1.0 (2013-12-14)

- fork off of basketweaver
  (https://code.google.com/p/basket-weaver/)
- deduce project name from filename alone, never extract a package
- include wheel packages in the index
- add python33 support
- add test suite
- rewrite readme
