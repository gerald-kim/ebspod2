Flask skeleton for google app engine. using buildout.

Setup
=====

::

  $ git clone https://github.com/utahta/flask-gae-template.git
  $ curl -LO http://svn.zope.org/*checkout*/zc.buildout/trunk/bootstrap/bootstrap.py
  $ python bootstrap.py -d
  $ ./bin/buildout

Using
=====

::

  $ ./bin/dev_appserver src/

Testing
======

::

  $ ./bin/test


TODO
====

chef cookbook -> mimms, ffmpeg, curl, libavcodec-extra-53