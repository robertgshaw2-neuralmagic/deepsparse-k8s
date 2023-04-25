FROM ghcr.io/neuralmagic/deepsparse:1.4.2

CMD sparsezoo.download --save-dir ./model zoo:nlp/sentiment_analysis/obert-base/pytorch/huggingface/sst2/pruned90_quant-none

CMD mv ./model/deployment ./deployment

CMD rm -rf ./model

ENTRYPOINT deepsparse.server --task sentiment-analysis --model_path ./deployment