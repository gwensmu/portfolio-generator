./generate --output_dir site
aws s3 sync site s3://textile.gwensmuda.com --acl public-read
