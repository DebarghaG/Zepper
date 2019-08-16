# Zepper

![License Badge](https://img.shields.io/github/license/DebarghaG/Zepper?style=plastic)
![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)

Zepper is a fun and simple asynchronous WSGI web server.

It's performance is not bad, and optimizations will be rolled out in the form of updates.

Zepper forms the testing bed for the decentralised applications being created with [Delta Tech Labs'](www.dtlabsindia.com) [TRST Technology](https://trst.dtlabsindia.com).

You can use v1.3 onwards as a somewhat reliable server, however please note that this is not production ready and is for experimental purposes only.

## Requirements

* Python 3.7+ (Tested Ubuntu 18.04)
* Make sure the following work
   * errno
   * os
   * signal
    * socket
    * sys
    * io

Follow the comments, commands and documentation incrementally while going through the first few versions of the release, and the tests to learn how to build a web server yourself.

## WSGI Workflow ( Server side )

* First, the server starts and loads an ‘application’ callable provided by your Web framework/application
* Then, the server reads a request
* Then, the server parses it
* Then, it builds an ‘environ’ dictionary using the request data
* Then, it calls the ‘application’ callable with the ‘environ’ dictionary and a ‘start_response’ callable as parameters and gets back a response body.
* Then, the server constructs an HTTP response using the data returned by the call to the ‘application’ object and the status and response headers set by the ‘start_response’ callable.
And finally, the server transmits the HTTP response back to the client

## Optimizations

Deals with the problems in load balancing of server by incorporating
* Simultaneous asynchronous requests
* Killing zombie processes
* Dealing with Orphan processes

## Author :

[@DebarghaG](www.debarghaganguly.com)

## Acknowledgements and References:

- Unix Network Programming, Volume 1: The Sockets Networking API (3rd Edition)

- Advanced Programming in the UNIX Environment, 3rd Edition

- The Linux Programming Interface: A Linux and UNIX System Programming Handbook

- PEP 333 — Python Web Server Gateway Interface

- Ruslan Spivak
