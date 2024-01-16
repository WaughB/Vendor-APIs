import requests
import yaml
import logging
from logger import log_this
import boto3
from botocore.exceptions import BotoCoreError, ClientError

logger = log_this(__name__, level=logging.DEBUG)
logger.info("S3 Uploader initialized")


class S3Uploader:
    """
    A utility class for uploading data to an AWS S3 bucket.

    This class handles the connection to AWS S3 and provides methods for
    uploading data to a specified S3 bucket.

    Attributes
    ----------
    s3_client : boto3.client
        The boto3 S3 client instance.
    bucket_name : str
        The name of the S3 bucket where data will be uploaded.

    Parameters
    ----------
    bucket_name : str
        The name of the S3 bucket to upload data to.
    """

    def __init__(self, bucket_name):
        """
        Initializes the S3Uploader instance with the specified bucket.

        Parameters
        ----------
        bucket_name : str
            The name of the S3 bucket to upload data to.
        """
        self.s3_client = boto3.client("s3")
        self.bucket_name = bucket_name
        logger.info("S3 Uploader initialized")

    def upload_data_to_s3(self, data, key):
        """
        Uploads data to the specified S3 bucket.

        Parameters
        ----------
        data : str or bytes
            The data to be uploaded to S3.
        key : str
            The S3 object key (file name) under which the data will be stored.

        Returns
        -------
        dict or None
            The response from the S3 put_object request, or None if an error occurs.

        Raises
        ------
        BotoCoreError, ClientError
            If errors occur while trying to upload to S3.
        """
        try:
            response = self.s3_client.put_object(
                Body=str(data), Bucket=self.bucket_name, Key=key
            )
            logger.info(f"Data uploaded to {self.bucket_name}/{key}")
            return response
        except (BotoCoreError, ClientError) as error:
            self.log_s3_upload_error(error)
            return None

    def log_s3_upload_error(self, error):
        """
        Logs an error that occurred during data upload to S3.

        This method is called internally by the upload_data_to_s3 method
        when an error is encountered.

        Parameters
        ----------
        error : BotoCoreError or ClientError
            The exception raised during the upload process.
        """
        logger.error(f"Error uploading data to S3: {error}")
