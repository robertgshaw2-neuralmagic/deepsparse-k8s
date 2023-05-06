FROM python:3.10-slim-buster

COPY deepsparse-whl /home/deepsparse-whl

RUN pip3 install /home/deepsparse-whl/deepsparse_nightly-1.5.0.20230503-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl[server]

RUN deepsparse.transformers.run_inference --help

RUN sparsezoo.download --save-dir ./model zoo:nlp/sentiment_analysis/obert-base/pytorch/huggingface/sst2/pruned90_quant-none

RUN mv ./model/deployment ./deployment

RUN rm -rf ./model

ENTRYPOINT deepsparse.server --task sentiment-analysis --model_path ./deployment
