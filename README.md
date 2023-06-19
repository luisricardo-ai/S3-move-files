# AWS S3 move files to a folder and delete object versioning

This code was built to move certain files with the same start name. You can use this in AWS lambda, so take a look in `event.json` there you will find the params to execute the `app.py` code.

The event structure is:

* bucket: Only the bucket name.
* prefix: Prefix of the folder where your folders that have the files are located.
* destination_folder: Only the name of the destination folder.
* folder_origin: List of the folders's name that have the files.
* partial_object_name: Common string between the names of the files you want to move