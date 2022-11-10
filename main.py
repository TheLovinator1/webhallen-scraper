"""
This program downloads the JSON from https://www.webhallen.com/api/product/ and adds it to MongoDB.
"""
import dataclasses
import os
import sys
from json import JSONDecodeError

import httpx
import rich
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.results import InsertOneResult
from rich.progress import track

# Take environment variables from .env.
load_dotenv(verbose=True)

# Our configuration
mongo_uri = os.getenv("MONGO_URI", None)
id_start = os.getenv("PRODUCT_ID_START", 1)
id_end = os.getenv("PRODUCT_ID_END", 380000)

if mongo_uri is None:
    sys.exit("Please fill out the .env or add an environment variable for MONGO_URI.")

print(f"MongoDB URI: {mongo_uri!r}")
print(f"I will download everything between {id_start} and {id_end} :-)")

# Connect to MongoDB
client = MongoClient(mongo_uri)

# Our database
db = client.openpricecomparison

# Group everything from Webhallen
webhallen = db.webhallen

# How many products to download
how_many = range(int(id_start), int(id_end))


@dataclasses.dataclass
class ResponseAndError:
    """
    Attributes
        response: httpx Response from the Webhallen API.
        err_msg: The error message, if error.
    """
    response: httpx.Response = None
    err_msg: str = ""


@dataclasses.dataclass
class JSONAndError:
    """
    Attributes
        json: The JSON.
        err_msg: The error message, if error.
    """
    json = None
    err_msg: str = ""


def get_product_json(product_response) -> JSONAndError:
    """
    Get the json from the response.

    Args:
        product_response: The response from the API.

    Returns:
        JSONAndError
    """
    try:
        # httpx has the response as JSON that we can use
        product_json = product_response.json()

    except JSONDecodeError as exc:
        return JSONAndError(err_msg=f"[red]{product_id} - Failed to decode JSON: {exc}")
    except TypeError as exc:
        return JSONAndError(err_msg=f"[red]{product_id} - Failed for {exc}")

    # Check if product_json is empty
    if not product_json:
        return JSONAndError(err_msg=f"[yellow]{product_id} was empty. Skipping!")

    return JSONAndError(product_json)


def check_if_in_database(product_num: int) -> bool:
    """
    Check if we already have this product in our database.

    Returns:
        True if in MongoDB database.
    """

    if webhallen.find_one({"product.id": int(product_num)}):
        rich.print(f"[yellow]{product_num} was already in the database. Skipping!")
        return True
    elif webhallen.find_one({"id": int(product_num)}):
        rich.print(f"[yellow]{product_num} was already in the database. Skipping!")
        return True

    return False


def get_json(product_num: int) -> ResponseAndError:
    """
    Get the product from the api.

    Args:
        product_num: The product ID.

    Returns:
        ResponseAndError
    """

    try:
        response: httpx.Response = httpx_client.get(f'https://www.webhallen.com/api/product/{product_num}')
    except httpx.RequestError as exc:
        return ResponseAndError(err_msg=f"[red]An error occurred while requesting {exc.request.url!r}.")

    return ResponseAndError(response)


if __name__ == "__main__":
    with httpx.Client() as httpx_client:
        for product_id in track(how_many, description="Downloading..."):
            # Check if we already have this product in our database.
            if check_if_in_database(product_id):
                continue

            # Get the product from the api.
            our_response = get_json(product_id)

            # Continue the loop if we get an error.
            if our_response.err_msg:
                rich.print(our_response.err_msg)
                continue

            # Our response from the API.
            r = our_response.response

            #  Get the json from the response.
            product_data = get_product_json(r)
            if product_data.err_msg:
                rich.print(product_data.err_msg)
                continue

            # Print the json
            rich.print_json(data=product_data.json)

            # Add the product to the mongodb
            product: InsertOneResult = webhallen.insert_one(product_data).inserted_id
