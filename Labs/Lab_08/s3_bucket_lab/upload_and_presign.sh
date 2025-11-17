#!/bin/bash

# $1 = local file
# $2 = bucket name
# $3 = expiration seconds

local_file=$1
bucket=$2
expires=$3

# upload file
aws s3 cp "$local_file" s3://"$bucket"/

# presign
aws s3 presign s3://"$bucket"/"$local_file" --expires-in "$expires"
