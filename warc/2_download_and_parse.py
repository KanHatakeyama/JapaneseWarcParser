"""
Based on the path list downloaded from CommonCrawl

1) Download warc.gz path, convert to warc file

2) Load the warc file and search for only Japanese sites,
  Extract information from that site

3) Combine the text of each tag

4) Annotate usable and unusable texts based on fasttext
"""
import sys
import random
import argparse
sys.path.append("../")

from tqdm import tqdm
from datasets import load_dataset

from src.cleaner.LineChecker import remove_dup_lines, remove_multi_headers
from src.cleaner.WordIntegrator import WordIntegrator
from src.cleaner.PerplexityChecker import PerplexityChecker
from src.file_utils import make_dir
from src.parse_warc import extract_japanese_from_warc
from src.downloader import get_cc_path_list, download_warc_file
if True:
    from mc4s.src.classifier.DatasetAnnotator import DatasetAnnotator
    from mc4s.src.cleaner.auto_cleaner import clean_text


def download_and_parse(cc_path, is_clean=False, base_dir=None):
    # download warc file
    warc_path = download_warc_file(cc_path)

    # parse warc file
    print("parsing "+warc_path)
    try:
        tag_records = extract_japanese_from_warc(warc_path)
        if is_clean:
            # clean
            cleaned_records = []
            for id in range(len(tag_records)):
                record = tag_records[id]
                lines = [i[0].strip() for i in record["text"]]
                lines = integrator(lines)
                txt = "\n".join(lines)
                if txt != "":
                    cleaned_records.append(
                        {"url": record["url"], "timestamp": record["timestamp"], "text": txt})

            # classify and save
            for record in cleaned_records:
                is_noise = annotator.predict(record["text"])
                if is_noise == 1:
                    continue
                filename = warc_path.split("/")[-1].replace(".warc", "")
                save_path = f"{corpus_dir}/{filename}.txt"
                with open(save_path, "a") as f:
                    f.write(str(record)+"\n")
            print("done "+warc_path)
        else:
            save_dict = {
                "tag_records" : tag_records,
                "cc_path" : cc_path,
                "warc_path" : warc_path
            }
            file_name = os.path.basename(warc_path)
            base_name = os.path.splitext(file_name)[0]
            file_base_name = "_".join(base_name.split("_")[2:])
            if base_dir is None:
                base_dir = "/tmp"
            os.makedirs(base_dir, exist_ok=True)
            save_gz_path = f"{base_dir}/{file_base_name}_japanese.json.gz"
            with gzip.open(save_gz_path, 'wt', encoding="ascii") as zipfile:
               json.dump(save_dict, zipfile)
        # clear warc file
        with open(warc_path, "w") as f:
            f.write("")
    except Exception as e:
        print("fail loading "+warc_path)
        return 


def main():
    """
    Parameter 
    -------------
    seed :
        Path list shuffle seed
    is_clean : 
        Flag for whether to perform data cleaning
    batch_number :
        Identification number when processing the path list by dividing it
        if batch_number = -1, run all paths 
    """
    # argparse
    parser = argparse.ArgumentParser(
            "Download/unzip/process the Japanese language of the downloaded commoncrawl gz path")
    parser.add_argument("--is_clean", type=bool, default=True, help="Flag for whether to perform data cleaning")
    parser.add_argument("batch_number", default=-1, type=int, 
                        help="Identification number when processing the path list by dividing it")
    args = parser.parse_args()

    # integrator for integrating text split by tag
    integrator = WordIntegrator(
        checker=PerplexityChecker("data/lm_sp/ja.arpa.bin",
                                  "data/lm_sp/ja.sp.model",
                                  ),
        filter_path="dict/header_filter.txt",
        start_filter_path="dict/start_filter.txt",
        end_filter_path="dict/end_filter.txt"
    )
    # annotator for classifying text
    dataset = load_dataset('mc4', 'ja', split='train', streaming=True)
    annotator = DatasetAnnotator(dataset, clean_func=clean_text, n_preload=500,
                                 out_path="../mc4s/annotations"
                                 )
    corpus_dir = "data/corpus"
    make_dir(corpus_dir)

    # get path list
    cc_path_list = get_cc_path_list()
    start_idx, end_idx = args.batch_number * 3, (args.batch_number+1) * 3
    target_path_list  = cc_path_list[start_idx:end_idx]
    save_dir = f"data/japanese_record/batch{args.batch_number}"
    submit_dir = f"data/japanese_record_submit/batch{args.batch_number}"
    for cc_path in tqdm(target_path_list):
        download_and_parse(cc_path, is_clean=args.is_clean, base_dir=save_dir)
    shutil.make_archive(submit_dir,
                        format='zip', root_dir=save_dir)

if __name__ == "__main__":
    main()