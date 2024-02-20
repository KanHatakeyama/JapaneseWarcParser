from src.file_utils import make_dir
import glob
from src.parse_warc import extract_japanese_from_warc
import json
import gzip
import time

"""
extract japanese pages from warc files

"""
make_dir("data/jap_dump")
done_list = []
while True:

    for path in glob.glob("data/warc/*.warc"):
        if path in done_list:
            continue
        print("try:" + path)
        with open(path, 'rb') as stream:
            string = stream.read()
        if len(string) == 0:
            print(f"empty file:{path}")
            done_list.append(path)
        try:
            ja_soup_list = extract_japanese_from_warc(path)
        except Exception as e:
            print("fail loading "+path)

        filename = path.split("/")[-1]
        filename.split(".")[0]
        filename = filename+"_jap.gz"

        with gzip.open(f'data/jap_dump/{filename}.gz', 'wt', encoding='utf-8') as f:
            json.dump(ja_soup_list, f, ensure_ascii=False)

        with open(path, "w") as f:
            f.write("")

    time.sleep(300)
