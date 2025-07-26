# Import required libraries
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
import pandas as pd


def is_valid_url(url):
    """
    Validates if the provided URL has proper structure.

    Args:
        url (str): URL to validate

    Returns:
        bool: True if URL has both scheme (http/https) and netloc (domain), False otherwise
    """
    parsed = urlparse(url)
    return all([parsed.scheme, parsed.netloc])


def is_url_reachable(url):
    """
    Checks if the URL is accessible and returns a successful response.

    Args:
        url (str): URL to check reachability

    Returns:
        bool: True if URL returns status code 200, False otherwise
    """
    try:
        response = requests.head(url, timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False


def save_output(car_data):
    """
    Saves the scraped car data to a CSV file.

    Args:
        car_data (dict): Dictionary containing car information with lists as values
    """
    car_list_df = pd.DataFrame.from_dict(car_data)
    car_list_df.to_csv("output_py.csv", index=False)


def extract_car_details(url=""):
    """
    Main function to scrape car details from the provided URL.

    Args:
        url (str): URL of the car listing page to scrape
    """
    # Validate URL format
    if not is_valid_url(url):
        print("Invalid URL! Please pass correct URL.")
    # Check if URL is accessible/scrapable
    elif not is_url_reachable(url):
        print("URL is not scrapable!")
    else:
        # Initialize data structure for car information
        car_data = {
            "brand": [],
            "model": [],
            "body_type": [],
            "model_seat": [],
            "model_variant": [],
            "price": [],
            "fuel_type": [],
            "transmission_type": [],
            "colour_variants": [],
            "location": [],
        }

        # Get webpage content
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        # Find all car listings
        car_list = soup.find_all("div", {"data-testid": "listingcardesktop"})

        # Extract data from each car listing
        for car in car_list:
            car_data["brand"].append(
                car.find("h2")
                .find("span", {"class": "styles__Make-sc-a6403e05-5 etWSJY"})
                .get_text()
            )
            car_data["model"].append(
                car.find("h2")
                .find("span", {"class": "styles__ModelName-sc-a6403e05-6 hGuUnc"})
                .get_text()
            )
            car_data["body_type"].append(
                car.find("p", {"data-testid": "car_model_body_type"}).get_text()
            )
            car_data["model_seat"].append(
                car.find("p", {"data-testid": "car_model_seat"}).get_text()
            )
            car_data["model_variant"].append(car.find("h3").get_text())
            car_data["price"].append(
                car.find(
                    "div", {"class": "styles__Price-sc-a6403e05-18 bsWAfs"}
                ).get_text()
            )
            car_data["fuel_type"].append(
                car.find("p", {"data-testid": "car_variant_fuel_type"}).get_text()
            )
            car_data["transmission_type"].append(
                car.find("p", {"data-testid": "car_variant_transmission"}).get_text()
            )
            car_data["colour_variants"].append(
                car.find_all(
                    "p", {"class": "styles__ParaWithoutMargins-sc-a6403e05-34 iAPjDz"}
                )[5].get_text()
            )
            car_data["location"].append(
                car.find_all(
                    "div", {"class": "styles__CityName-sc-a6403e05-17 fZrHFu"}
                )[0]
                .get_text()
                .split()[1]
            )

        # Save the extracted data to CSV file
        save_output(car_data)


# Execute the scraper
extract_car_details(url="https://ackodrive.com/collection/tata-cars/")
