#!/bin/bash
# cleanup.sh — removes the AWS resources created by this project.
# Usage: bash cleanup.sh

BUCKET="claim-documents-poc-sha"   # change to your bucket name

echo "This will permanently delete the bucket: $BUCKET"
read -p "Are you sure? (yes/no) " confirm

if [ "$confirm" = "yes" ]; then
    aws s3 rb s3://$BUCKET --force
    echo "Bucket $BUCKET deleted."
else
    echo "Cancelled. Nothing was deleted."
fi
