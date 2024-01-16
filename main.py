import requests
import yaml
import logging
from logger import log_this
import boto3
from botocore.exceptions import BotoCoreError, ClientError
from s3_uploader import S3Uploader
from github_api import GitHubAPI


def load_configuration(file_name):
    """
    Loads configuration from a specified YAML file.

    Parameters
    ----------
    file_name : str
        The path to the YAML configuration file.

    Returns
    -------
    dict
        A dictionary containing the loaded configuration.
    """
    with open(file_name, "r") as file:
        logger.debug(f"Loading configuration from {file_name}")
        logger.debug(f"Configuration: {yaml.safe_load(file)}")
        logger.debug("Configuration loaded successfully")
        return yaml.safe_load(file)


def upload_github_data_to_s3(api_client, uploader, username):
    """
    Fetches data from GitHub and uploads it to an AWS S3 bucket.

    This function retrieves user details and repositories from GitHub using the provided API client,
    then uploads the data to an S3 bucket using the provided uploader.

    Parameters
    ----------
    api_client : GitHubAPI
        An instance of the GitHubAPI class to interact with the GitHub API.
    uploader : S3Uploader
        An instance of the S3Uploader class to handle uploading data to S3.
    username : str
        The GitHub username for which to fetch and upload data.

    Raises
    ------
    Exception
        Any exceptions that occur during the data fetching or uploading process.
    """
    try:
        user_details = api_client.get_user_details(username)
        user_repos = api_client.get_user_repos(username)

        uploader.upload_data_to_s3(user_details, f"{username}_details.json")
        uploader.upload_data_to_s3(user_repos, f"{username}_repos.json")

        logger.info(f"User Details and Repositories for '{username}' uploaded to S3")
    except Exception as e:
        logger.error(f"An error occurred during data fetching or uploading: {e}")


# Main execution
if __name__ == "__main__":
    logger = log_this(__name__, level=logging.DEBUG)
    logger.info("Program started.")
    config = load_configuration("config.yml")
    github_base_url = config["github_base_url"]
    github_token = config["github_token"]
    github_api_client = GitHubAPI(github_base_url, github_token)
    # s3_uploader = S3Uploader(config["s3_bucket_name"])
    # upload_github_data_to_s3(github_api_client, s3_uploader, "octocat")
