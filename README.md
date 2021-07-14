# Server_V2
This project is a rewrite of a previous learning project.
I decided to make it much cleaner and better and will probably continue to update this in the future.

It uses simpleHTTPServer to process the requests with multithreading
The test client is used for testing all the functions inside the server and draws the IP address from a .env file

I will probably add support for running python files at request and retrieving the output.

#Instructions
Requests to the server are made in the format "http://{ip}:{port}/{request}"
eg: "http://127.0.0.1:8084/fileUpload.html"
This request will work for all files in the "files" folder
(provided it is contained in the same directory as the running program)

Compile.bat is also included to compile the source code into a working executable.
Note that currently there is no external config file for the server so you cannot change the port number
without recompiling the program.

This program uses infi.systray to make the console always available 
and it is possible to hide the console using the systray icon.

Colorama is also used in this program to make information and errors more distinguishable.

I will likely continue to improve this for some time.

#Purpose
I mainly use this program for running functions remotely (like from my phone)
and for transferring large files between devices. 
For example if you need to transfer a file between 2 devices, you can use the server as a bridge,
uploading the file to the server using fileUpload.html and then use the direct link to that file to download
it on the second device.

#Issues
If running this from inside a command prompt, make sure to change the working directory to the location of the program
before running, otherwise it will think it's in a different place to where it really is