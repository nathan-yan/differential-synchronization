# differential-synchronization
An implementation of scalable differential synchronization for collaboration.

## What is differential synchronization? ##
Differential synchronization is a way of keeping documents on different computers the same. Users should be able to make independent changes on their own copies of the document, and differential synchronization will copy those changes onto all other documents so that they're all the same.

Differential synchronization can be explained in more detail [here](https://neil.fraser.name/writing/sync/).

## How to use ##
The application of diff-sync used in this repo is for code, but can be repurposed for any other type of content. There are two files, __diff_server.py__ and __test.html__. __test.html__ is the client interface for diff-sync, which is what the user will be able to type on. __diff_server.py__ is the server that handles all changes made by a user and sends it to other connected users. 

To run, change the host ip address in __diff_server.py__ to your local ip address, then 
```
python diff_server.py
```

Then change the connection host ip address is __test.html__ to the server's local ip address, then open __test.html__

