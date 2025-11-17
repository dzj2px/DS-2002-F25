import boto3
import requests

bucket = "ds2002-f25-dzj2px"
url = "https://httpbin.org/image/png"
object_name = "remote_image.png"
expires = 300 # 5 minutes

# download file
r = requests.get(url)
open(object_name, "wb").write(r.content)

# upload to S3 (private)
s3 = boto3.client("s3", region_name="us-east-1")
s3.upload_file(Filename=object_name, Bucket=bucket, Key=object_name)

# presign URL
link = s3.generate_presigned_url(
    ClientMethod="get_object",
    Params={"Bucket": bucket, "Key": object_name},
    ExpiresIn=expires
)

print("Presigned URL:", link)
