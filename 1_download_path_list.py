from src.file_utils import download_file, decompress_gz, make_dir

"""
download path list from commoncrawl
"""

path_urls = [
    "https://data.commoncrawl.org/crawl-data/CC-MAIN-2023-50/warc.paths.gz",
    # "https://data.commoncrawl.org/crawl-data/CC-MAIN-2022-49/warc.paths.gz",
]


make_dir("data")
make_dir("data/path_list")

for url in path_urls:
    file_name = url.split("/")[-2]+".gz"
    download_file(url, f"data/path_list/{file_name}")
    decompress_gz(f"data/path_list/{file_name}",
                  f"data/path_list/{file_name.split('.')[0]}")
