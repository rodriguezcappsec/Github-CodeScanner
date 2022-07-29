from pickle import TRUE
from bs4 import BeautifulSoup
import re
import requests
import click
from urllib.parse import urljoin


all_files = []
all_main_directories = []
TARGET = "https://github.com/"
RAW_CONTENT = "https://raw.githubusercontent.com/"
headers = ""


@click.command()
@click.option("--username", required=True, type=str, help="repository username owner")
@click.option("--reponame", required=True, type=str, help="name of the repository")
@click.option("--tree", required=False, type=str, help="don't use it... is for recursive shit...")
def get_main_repo_trees_blobs(username, reponame, tree):
    click.echo(f"Crawling github repo {click.style(TARGET, fg='green')}... \n\n")
    try:
        page = requests.get(f"{TARGET}{username}/{reponame}", headers=headers if headers != None else "")
        if page.status_code == 200:
            soup = BeautifulSoup(page.text, "html.parser")
            main_container = soup.find("div", {"aria-labelledby": "files"})
            for a in main_container.find_all("a", {"data-pjax": "#repo-content-pjax-container"}):
                link = str(a.get("href"))
                if "/tree/" in link and "/node_modules" not in link:
                    all_main_directories.append(urljoin(TARGET, link).replace("\r\n\t", "").strip())
                if "/blob/" in link:
                    all_files.append(urljoin(RAW_CONTENT, link).replace("/blob/", "/").replace("\r\n\t", "").strip())
        else:
            page.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print("Http Error:", e)
    except requests.exceptions.ConnectionError as ce:
        print("Error Connecting:", ce)
    recursive_file_discovery(all_main_directories)
    print(all_files)


def recursive_file_discovery(folder_array):
    try:
        for folder in folder_array:
            page = requests.get(folder, headers=headers if headers != None else "")
            if page.status_code == 200:
                soup = BeautifulSoup(page.text, "html.parser")
                main_container = soup.find("div", {"aria-labelledby": "files"})
                for a in main_container.find_all("a", {"data-pjax": "#repo-content-pjax-container"}):
                    link = str(a.get("href"))
                    if "/tree/" in link and "/node_modules" not in link:
                        recursive_file_discovery([urljoin(TARGET, link).replace("\r\n\t", "").strip()])
                    if "/blob/" in link:
                        all_files.append(
                            urljoin(RAW_CONTENT, link).replace("/blob/", "/").replace("\r\n\t", "").strip()
                        )

            else:
                page.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print("Http Error:", e)
    except requests.exceptions.ConnectionError as ce:
        print("Error Connecting:", ce)


if __name__ == "__main__":
    get_main_repo_trees_blobs()
