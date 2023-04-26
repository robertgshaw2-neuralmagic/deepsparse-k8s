FROM ghcr.io/neuralmagic/deepsparse:1.4.2

RUN sparsezoo.download --save-dir ./model zoo:nlp/sentiment_analysis/obert-base/pytorch/huggingface/sst2/pruned90_quant-none

RUN mv ./model/deployment ./deployment

RUN rm -rf ./model

ENTRYPOINT deepsparse.server --task sentiment-analysis --model_path ./deployment --num-cores 4
