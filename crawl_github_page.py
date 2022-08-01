from bs4 import BeautifulSoup
import requests
import click
from urllib.parse import urljoin
import scanners

all_files = []
all_main_directories = []
TARGET = "https://github.com/"
RAW_CONTENT = "https://raw.githubusercontent.com/"
headers = ""


@click.command()
@click.option("--username", required=True, type=str, help="repository username owner")
@click.option("--reponame", required=True, type=str, help="name of the repository")

def get_main_repo_trees_blobs(username, reponame):
    tar = f"{TARGET}{username}/{reponame}"
    click.echo(f"Crawling github repo {click.style(tar, fg='green')}... \n\n")
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
                    """
                    Scan here boi...
                    """
                    all_files.append(urljoin(RAW_CONTENT, link).replace("/blob/", "/").replace("\r\n\t", "").strip())
        else:
            page.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print("Http Error:", e)
    except requests.exceptions.ConnectionError as ce:
        print("Error Connecting:", ce)
    recursive_file_discovery(all_main_directories)
    print(all_files)
    fetch_files(all_files)


def fetch_files(files_array):
    for index, file in enumerate(files_array):
        data = requests.get(file, headers=headers if headers != None else "")
        # print(data.text) // content of files here.
        break


def recursive_file_discovery(folder_array):
    try:
        for folder in folder_array:
            page = requests.get(folder, headers=headers if headers != None else "")
            if page.status_code == 200:
                soup = BeautifulSoup(page.text, "html.parser")
                main_container = soup.find("div", {"aria-labelledby": "files"})
                for a in main_container.findChildren("a", {"data-pjax": "#repo-content-pjax-container"}):
                    link = str(a.get("href"))
                    if "/tree/" in link and "/node_modules" not in link:
                        recursive_file_discovery([urljoin(TARGET, link).replace("\r\n\t", "").strip()])
                    if "/blob/" in link:
                        """
                        Scan here boi...
                        """
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
