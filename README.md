## **MagicBloodHound**

### Project description
A python3 script created to ingest data into BloodHound CE (Community Edition).

### Dependencies
You can install the python3 dependencies using the requeriments.txt file:
```pip3 install -r requirements.txt```

This python script is developed for linux systems. This is the dependencies that the script needs to work fine:

   - dd
   - unzip
   - rm
   
### Usage

![alt text](https://raw.githubusercontent.com/magichk/magicbloodhound/master/images/help.png "MagicBloodHound - Help")

You need to change the credentials in the script with your BloodHound UI credentials:

![alt text](https://raw.githubusercontent.com/magichk/magicbloodhound/master/images/configuration.png "MagicBloodHound - Configuration")

After that, run the script and wait for the results. In the following example, I have used a machine of Hackthebox platform named Blackfield.  When the tool finishes, BloodHound is ingesting the uploaded data. In the administration panel you can see when the ingestion is finished.

![alt text](https://raw.githubusercontent.com/magichk/magicbloodhound/master/images/tool.png "MagicBloodHound - Running")

![alt text](https://raw.githubusercontent.com/magichk/magicbloodhound/master/images/ingesting.png "MagicBloodHound - Ingesting")

![alt text](https://raw.githubusercontent.com/magichk/magicbloodhound/master/images/ingested.png "MagicBloodHound - Ingested")

In order to check that the process is going well, you can see the docker logs of a BloodHound container. When the ingest is correct, you will see a log like the following example:

![alt text](https://raw.githubusercontent.com/magichk/magicbloodhound/master/images/dockerlog.png "MagicBloodHound - Docker Log")

Finally, this is an example about the ingested data.

![alt text](https://raw.githubusercontent.com/magichk/magicbloodhound/master/images/example.png "MagicBloodHound - Example")

You can search what users has a path to Domain Admins group.

![alt text](https://raw.githubusercontent.com/magichk/magicbloodhound/master/images/pathtoda.png "MagicBloodHound - Path to Domain Admins group")

### How it works?

By default, the collectors of BloodHound CE create a zip file with the json data as the classic BloodHound. When I tried to upload individually the .json files with the UI worked fine, but when I tried with API always returned an error about encoding or special characters. The reason is that the first 3 bytes of every single file are "ef bb bf". To solve this problem, a new file using dd command is created during the execution of the script in order to avoid this three bytes. After importing, the program will delete these new files. For this reason, if the files are big, the tool will spend a large amount of time to process. I will improve this point in the future to spend less time in the dd operation.

- Unzip BloodHoud ZIP data.
- Avoid the first three bytes of every json creating a new file named <file>.json-bh 
- Import this file to BloodHound using the API with 3 requests. 
- Delete the new files with "-bh" that I created previously with dd.
- Delete the extracted .json files.


