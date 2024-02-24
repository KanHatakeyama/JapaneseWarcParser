FROM python:3.10

# 現在のレポジトリをコンテナに移す
WORKDIR /app
COPY . /app

# 基本的なライブラリのinstall
RUN pip install requests
RUN pip install fasttext
RUN pip install warcio
RUN pip install beautifulsoup4
RUN pip install tqdm
RUN pip install bunkai
RUN pip install emoji==1.7.0
RUN pip install nltk
RUN pip install mecab-python3
RUN pip install ja-sentence-segmenter
RUN pip install datasets
RUN pip install hojichar
RUN pip install scikit-learn
RUN pip install python-tlsh

# Mecabのinstall 
RUN apt update
RUN apt install mecab -y
RUN apt install libmecab-dev -y
RUN apt install mecab-ipadic-utf8 -y
RUN ln -s /etc/mecabrc /usr/local/etc/mecabrc #https://hakasenote.hnishi.com/2020/20200719-mecab-neologd-in-colab/
RUN pip install mecab-python3

#fasttext 記事のフィルタリングに使用する
RUN pip install gensim
RUN mkdir -p /app/mc4s/annotations/text_labels/
RUN cd /app/mc4s/annotations/text_labels/ && wget https://dl.fbaipublicfiles.com/fasttext/vectors-crawl/cc.ja.300.bin.gz && gzip -d cc.ja.300.bin.gz

#kenlm  warcファイルの解析に使用する
#https://zenn.dev/syoyo/articles/529ce949121ca4
RUN apt install build-essential cmake libboost-system-dev libboost-thread-dev -y
RUN apt install libboost-program-options-dev libboost-test-dev -y
RUN apt install  libeigen3-dev zlib1g-dev libbz2-dev liblzma-dev -y 
RUN pip install https://github.com/kpu/kenlm/archive/master.zip
RUN python -m pip install sentencepiece "protobuf<3.20.*"
RUN mkdir -p /app/warc/data/lm_sp
RUN wget -c  -P /app/warc/data/lm_sp http://dl.fbaipublicfiles.com/cc_net/lm/ja.arpa.bin
RUN wget -c  -P /app/warc/data/lm_sp http://dl.fbaipublicfiles.com/cc_net/lm/ja.sp.model

#jupyter jupyter notebookを使って作業する
RUN pip install jupyter
EXPOSE 8701
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8701", "--no-browser", "--allow-root", "--NotebookApp.token=''"]