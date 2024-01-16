import requests
import yaml
import logging
from logger import log_this
import boto3
from botocore.exceptions import BotoCoreError, ClientError
from logger import log_this

logger = log_this(__name__, level=logging.DEBUG)
logger.info("GitHub API initialized")


class GitHubAPI:
    """
    A client for interacting with the GitHub API.

    This class provides methods to interact with various endpoints of the GitHub API.
    It handles the request making process, including setting appropriate headers and error handling.

    Attributes
    ----------
    base_url : str
        The base URL for the GitHub API.
    headers : dict
        Headers to include in API requests, particularly the authorization token.

    Methods
    -------
    make_request(endpoint, method="GET", params=None)
        Makes a request to a specified endpoint of the GitHub API.
    send_http_request(url, method, params)
        Sends an HTTP request to the provided URL.
    handle_request_error(error)
        Handles any errors that occur during an HTTP request.
    get_user_details(username)
        Fetches details of a specified GitHub user.
    get_user_repos(username)
        Fetches repositories of a specified GitHub user.
    """

    def __init__(self, base_url, token):
        """
        Initializes the GitHubAPI client with the provided base URL and personal access token.

        Parameters
        ----------
        base_url : str
            The base URL for the GitHub API.
        token : str
            Personal access token for the GitHub API.

        Notes
        -----
        The personal access token is used to authenticate requests to the GitHub API.
        """
        self.base_url = base_url
        self.headers = {"Authorization": f"token {token}"}
        logger.info("GitHub API client initialized")

    def make_request(self, endpoint, method="GET", params=None):
        """
                Makes a request to a specified endpoint of the GitHub API and returns the response.

                Parameters
                ----------
                endpoint : str
                    The API endpoint to make the request to.
                method : str, optional
                    The HTTP method to use for the
        request (default is "GET").
        params : dict, optional
        Any parameters to include in the request (default is None).

        python
        Copy code
            Returns
            -------
            dict or None
                The parsed JSON response from the GitHub API if the request is successful; None otherwise.

            Notes
            -----
            This method constructs the full URL by appending the endpoint to the base URL,
            sends the HTTP request, and handles the response.
        """
        url = self.base_url + endpoint
        logger.info(f"Making a {method} request to {url}")
        response = self.send_http_request(url, method, params)
        return response.json() if response else None

    def send_http_request(self, url, method, params):
        """
        Sends an HTTP request to the provided URL and handles any potential errors.

        Parameters
        ----------
        url : str
            The full URL to which the request is sent.
        method : str
            The HTTP method to use for the request.
        params : dict
            Any parameters to include in the request.

        Returns
        -------
        requests.Response or None
            The response object from the requests library if the request is successful; None otherwise.

        Raises
        ------
        requests.exceptions.RequestException
            Any exception raised by the requests library during the request.
        """
        try:
            response = requests.request(
                method, url, headers=self.headers, params=params
            )
            response.raise_for_status()
            logger.info("Request successful")
            return response
        except requests.exceptions.RequestException as error:
            self.handle_request_error(error)
            return None

    def handle_request_error(self, error):
        """
        Handles errors that occur during an HTTP request.

        Parameters
        ----------
        error : requests.exceptions.RequestException
            The exception raised during the HTTP request.

        Notes
        -----
        Logs the error using the configured logger.
        """
        logger.error(f"Error during request: {error}")

    def get_user_details(self, username):
        """
            Fetches details of a specified GitHub user.

            Parameters
            ----------
            username : str
                The GitHub username of the user whose details are to be fetched.

            Returns

        python
        Copy code
            dict or None
                The user's details as a dictionary if the request is successful; None otherwise.

            Notes
            -----
            Makes use of the `make_request` method to retrieve user details from the
            GitHub API's `/users/{username}` endpoint.
        """
        logger.info(f"Fetching user details for {username}")
        return self.make_request(f"users/{username}")

    def get_user_repos(self, username):
        """
        Fetches repositories of a specified GitHub user.

        Parameters
        ----------
        username : str
            The GitHub username of the user whose repositories are to be fetched.

        Returns
        -------
        list or None
            A list of repositories if the request is successful; None otherwise.

        Notes
        -----
        Makes use of the `make_request` method to retrieve the user's repositories from the
        GitHub API's `/users/{username}/repos` endpoint.
        """
        logger.info(f"Fetching repositories for {username}")
        return self.make_request(f"users/{username}/repos")
