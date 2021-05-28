import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass, asdict
from typing import List
import csv


@dataclass
class Post:
    link: str
    title: str
    category: str
    date: str


class NaszosieScrapper:

    def __init__(self) -> None:
        self.website = "https://naszosie.pl/"

    def scrape_site(self) -> List[Post]:
        try:
            response = requests.get(self.website).text
            soup = BeautifulSoup(response, "html.parser")
            posts = self.extract_posts_from_site(soup)
            return posts
        except Exception as e:
            print(f"There was w problem with {e}")
            pass

    def extract_posts_from_site(self, soup: BeautifulSoup) -> List[Post]:
        list_of_posts = []
        posts_in_header = soup.find_all("div", class_="td-big-grid-post")
        posts_in_body = soup.find_all("div", class_="td-block-span4")
        for post in posts_in_header:
            try:
                link = (post.find("a", class_="td-image-wrap").get("href"))
                title = (post.find("a", class_="td-image-wrap").get("title"))
                category = (post.find("a", class_="td-post-category").text)
                date = (post.find("span", class_="td-post-date").text)
                list_of_posts.append(
                    Post(link=link, title=title, category=category, date=date))
            except Exception as e:
                print(f"There was problem fetching this post: {e}")

        for post in posts_in_body:
            try:
                link = (post.find("a", class_="td-image-wrap").get("href"))
                title = (post.find("a", class_="td-image-wrap").get("title"))
                category = (post.find("a", class_="td-post-category").text)
                date = (post.find("span", class_="td-post-date").text)
                list_of_posts.append(
                    Post(link=link, title=title, category=category, date=date))
            except Exception as e:
                print(f"There was problem fetching this post: {e}")

        return list_of_posts


def scrape():
    scraper = NaszosieScrapper()
    result = scraper.scrape_site()
    write_to_csv(result)


def write_to_csv(posts: List[Post]) -> None:
    with open("posts.csv", mode="w") as file:
        fieldnames = [
            "link",
            "title",
            "category",
            "date"
        ]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for post in posts:
            writer.writerow(asdict(post))


if __name__ == "__main__":
    scrape()
