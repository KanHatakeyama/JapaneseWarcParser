from src.file_utils import download_file, decompress_gz, make_dir
import glob

"""
download warc files from commoncrawl list

"""


# load path list
path_list = []
for file_path in glob.glob("data/path_list/*"):
    print(file_path)
    with open(file_path, "r") as f:
        temp_path_list = f.readlines()

    temp_path_list = [path.strip() for path in temp_path_list]

    path_list += temp_path_list


# download files

base_url = "https://data.commoncrawl.org/"
make_dir("data/gz")
make_dir("data/warc")
for path in path_list:
    url = base_url+path

    filename = path.replace("/", "_")
    gz_path = f"data/gz/{filename}"
    warc_path = f"data/warc/{filename}".replace(".gz", "")
    try:
        download_file(url, gz_path)
        decompress_gz(gz_path, warc_path, remove_gz=False, fill_blank_gz=True)
    except Exception as e:
        print(e)
        print("fail loading "+url)
        continue
