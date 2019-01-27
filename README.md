To add images, put full-size images in the /images folder. The script will resize images to 800 x 600px as copies. Images smaller than 800px wide will not be resized, only copied.

An key for the image will automatically be entered into the static/descriptions.yml file. Update the value of that item to add a description to the image page.

To generate the site:
```
./generate --output-dir site-folder-name
```

To generate and deploy to AWS S3 in one step:

```
./deploy
```

