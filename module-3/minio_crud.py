from minio import Minio
from minio.error import S3Error

# docker run \
#    -p 9000:9000 \
#    -p 9001:9001 \
#    --user $(id -u):$(id -g) \
#    --name minio1 \
#    -e "MINIO_ROOT_USER=ROOTUSER" \
#    -e "MINIO_ROOT_PASSWORD=CHANGEME123" \
#    -v ${HOME}/minio/data:/data \
#    quay.io/minio/minio server /data --console-address ":9001"


class MinioClient:
    def __init__(self, endpoint, access_key, secret_key, secure=False):
        # Initialize the Minio client
        self.client = Minio(endpoint, access_key=access_key, secret_key=secret_key, secure=secure)

    def create_bucket(self, bucket_name):
        """Create a new bucket if it doesn't exist."""
        try:
            if not self.client.bucket_exists(bucket_name):
                self.client.make_bucket(bucket_name)
                print(f"Bucket '{bucket_name}' created successfully.")
            else:
                print(f"Bucket '{bucket_name}' already exists.")
        except S3Error as err:
            print(f"Error creating bucket: {err}")

    def upload_file(self, bucket_name, object_name, file_path):
        """Upload a file to a specified bucket."""
        try:
            self.client.fput_object(bucket_name, object_name, file_path)
            print(f"File '{file_path}' uploaded successfully as '{object_name}' to bucket '{bucket_name}'.")
        except S3Error as err:
            print(f"Error uploading file: {err}")

    def download_file(self, bucket_name, object_name, file_path):
        """Download a file from the specified bucket."""
        try:
            self.client.fget_object(bucket_name, object_name, file_path)
            print(f"File '{object_name}' downloaded successfully to '{file_path}'.")
        except S3Error as err:
            print(f"Error downloading file: {err}")

    def list_files(self, bucket_name):
        """List all files in the specified bucket."""
        try:
            objects = self.client.list_objects(bucket_name)
            print(f"Files in bucket '{bucket_name}':")
            for obj in objects:
                print(f" - {obj.object_name}")
        except S3Error as err:
            print(f"Error listing files: {err}")

    def delete_file(self, bucket_name, object_name):
        """Delete a file from the specified bucket."""
        try:
            self.client.remove_object(bucket_name, object_name)
            print(f"File '{object_name}' deleted from bucket '{bucket_name}'.")
        except S3Error as err:
            print(f"Error deleting file: {err}")

    def delete_bucket(self, bucket_name):
        """Delete the bucket if it is empty."""
        try:
            self.client.remove_bucket(bucket_name)
            print(f"Bucket '{bucket_name}' deleted successfully.")
        except S3Error as err:
            print(f"Error deleting bucket: {err}")


if __name__ == "__main__":
    minio_client = MinioClient(endpoint="0.0.0.0:9000", access_key="ROOTUSER", secret_key="CHANGEME123", secure=False)

    bucket_name = "python-test-bucket"
    file_path = "/tmp/test-file.txt"
    object_name = "my-test-file.txt"

    # Create a bucket
    minio_client.create_bucket(bucket_name)

    # Upload a file
    minio_client.upload_file(bucket_name, object_name, file_path)

    # List all files in the bucket
    minio_client.list_files(bucket_name)

    # Download the uploaded file
    minio_client.download_file(bucket_name, object_name, "/tmp/downloaded-file.txt")

    # Delete the uploaded file
    minio_client.delete_file(bucket_name, object_name)

    # Delete the bucket
    minio_client.delete_bucket(bucket_name)
