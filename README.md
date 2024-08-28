# poliris-portescles-wordpress
This repo contains code to get/convert/upload a poliris file from LesPortesCles to a format readable by a Wordpress plugin (Like WP AllImport)

# Python scripts
The python scripts downloads the poliris file directly from LesPortesCles using the data specified in link_list

If you plan on using the Cypress config for automating WP All Import you have to upload the file first through the interface, this will give you said hash which is a folder where the file will be uploaded everytime.
Also required for the Cypress config is the import id number which is in the URL when you click on "Import file" - example :
https://myurl.com/wp-admin/admin.php?page=pmxi-admin-manage&id=**ID**&action=update"

## Installation
After creating your secrets.json file and link_list.json file :
Simply pip -r requirements.txt then python3 main.py

# Cypress
The cypress part allows you to automatically run both the scripts and the upload without the need for the premium subscription of wp All Import

## Installation
npm install

## Usage
After configuring the secrets.json and config.json file you can launch it using npx cypress run