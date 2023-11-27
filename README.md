# File Sharing App

## Introduction
a simple file-sharing application with application protocols defined by each group, using the TCP/IP protocol stack. 

## Requirements
- Python 3 (see [https://www.python.org/downloads/](https://www.python.org/downloads/) for latest versions of Python)
- Tkinter: kinter can be installed using pip. The following command is run in the command prompt to install Tkinter.
pip install tk 

## Features
### Server
- Ping hostname: live check the host named hostname
- Discover hostname: discover the list of local files of the host named hostname
### Client
- Publish lname fname: a local file (which is stored in the client's file system at lname) is added to the
client's repository as a file named fname and this information is conveyed to the server.
- Fetch fname: fetch some copy of the target file and add it to the local repository.
## CLI User Guide
### Server:
- Ping command: ping {hostname}
- Discover hostname: discover {hostname}
### Client:
- Publish lname fname: ping {hostname}
- Discover hostname: discover {hostname}
### Client
- Publish: Publish {lname} {fname}
+ lname: path to the file to publish
+ fname: the name saved in the
client's repository
- Fetch: fetch {fname}
+ fname: The name of the file requested to fetch
