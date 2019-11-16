./generate --output site
aws s3 sync site s3://textile.gwensmuda.com --acl public-read
