"""Calls to an api asynchronously."""
# Standard Library Imports
from concurrent.futures import ThreadPoolExecutor
from timeit import timeit

# Third Party Imports
import requests
from requests.exceptions import HTTPError

# Local App Imports
from api_client import ApiClient

NUM_POSTS = list(range(1, 101))
URL = "https://jsonplaceholder.typicode.com"
ENDPOINT = "/posts"


def get_all_posts():
    api_client = ApiClient(URL)

    try:
        posts = api_client.get(ENDPOINT)
    except HTTPError as http_err:
        if http_err.response.status_code == 404:
            print("Not found")
        else:
            print(str(http_err))

        return None

    api_client.close()

    return posts


def get_all_posts_normal_call():
    normal_posts = []
    for post_id in NUM_POSTS:
        this_url = f"{URL}{ENDPOINT}/{post_id}"

        response = requests.get(this_url, timeout=30)

        normal_posts.append(response.json())

    return normal_posts


def get_all_posts_with_client():
    client_posts = []
    with ApiClient(URL) as api_client:
        for post_id in NUM_POSTS:
            client_posts.append(api_client.get(f"{ENDPOINT}/{post_id}"))
    return client_posts


def get_all_posts_with_threads():
    thread_posts = []
    with ApiClient(URL) as api_client:
        with ThreadPoolExecutor(max_workers=10) as executor:
            tasks = [executor.submit(api_client.get, f"{ENDPOINT}/{post_id}") for post_id in NUM_POSTS]
            for task in tasks:
                thread_posts.append(task.result())

    return thread_posts


if __name__ == "__main__":
    print("Normal Call:")
    print(f"\t{timeit(get_all_posts_normal_call, number=1)}")
    print("Call with Client")
    print(f"\t{timeit(get_all_posts_with_client, number=1)}")
    print("Thread Calls")
    print(f"\t{timeit(get_all_posts_with_threads, number=1)}")
