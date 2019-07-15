# SECURE PERSONAL CLOUD

## Clients

### Linux Client
* Linux Client is entirely written using combination of bash and python which directly interacts with Django mainserver
* The Linux Client needs to use a fully developed command tool "spc", supporting man pages, version-control, etc., to interact with the cloud
* For Uploading files via linux client, one needs to first observe the file and then sync them with the database
* The files available on the cloud are displayed using tree structure

### Web Client
* The Web-Client is entirely written using HTML,DTL and javascript
* The Web-Client contains a login page, a sign-up page and a profile page
* Files Uploaded on the Cloud can be viewed as well as downloaded using web-client

## Server

* Server is written entirely using Django Library
* It stores all the data in mySQL database in encrypted format
* Django project consists of 2 applications viz. mainserver, webcleint
* Main Server only handles all the POST requests made by linux client or during form submission and responds with a HTTPResponse
* Web-Client is just an extension of Main Server as it internally calls methods of Main Server, the only difference being it returns HTML response


## Installation Guide

* Execute- **sudo bash install.sh _[[directory where you wish to install it]]_**
* sudo is required for the installation of **man**
