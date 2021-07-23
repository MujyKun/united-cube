## UCube

### What is it?
UCube creates internal cache for the communities a user follows on [United-Cube](https://www.united-cube.com/).  
This is a **wrapper** for United-Cube's private API, but may be referred to as an API on this repository.



### **[API Documentation](https://ucube.readthedocs.io/en/latest/)**

### **[Discord Support Server](https://discord.gg/bEXm85V)**

**[A UCUBE DISCORD BOT CAN BE FOUND HERE](https://github.com/MujyKun/united-cube-bot)**  


### Functionalities

* Asynchronous and Synchronous Support
* Receive all the posts the artists in your communities have made. This includes all images/videos/comments made by them.
* Cache is split under a hierarchy directly under a community.  
* Keep track of notifications on your user account, you can easily create a loop to update your notification cache on updates. (Usage of this can be found in the examples folder)

### Installation

In a terminal, type `pip install ucube`.  

To install from source:  
`pip install git+https://github.com/MujyKun/united-cube.git`


### How to Use

There are two ways to log in.  
The first way is using a username and password to login which will automatically refresh your token.  
The second way is getting your account token manually and will require manual updates about every 6 months.

In order to get your account token, go to [United-Cube](https://www.united-cube.com/) and Inspect Element (F12).  
Then go to the `Network` tab and filter by `XHR`. Then refresh your page (F5) and look for `popup` or `clubs` under `XHR`.  
Under Headers, scroll to the bottom and view the request headers. You want to copy everything past `authorization: Bearer`.

For example, you may see (This is just an example):  
``Authorization: Bearer ABCDEFGHIJKLMNOPQRSTUVWXYZ``  
Then ``ABCDEFGHIJKLMNOPQRSTUVWXYZ`` would be your auth token for UCube. 
It is suggested to have the auth token as an environment variable.

#### CODE EXAMPLES

```python


# Asynchronous


# Synchronous


```
**[More Detailed Asynchronous Example](https://github.com/MujyKun/united-cube/blob/main/examples/asynchronous.py)**  
**[More Detailed Synchronous Example](https://github.com/MujyKun/united-cube/blob/main/examples/synchronous.py)**

### **[API Documentation](https://ucube.readthedocs.io/en/latest/)**