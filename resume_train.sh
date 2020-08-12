export CUDA_VISIBLE_DEVICES=0
onmt-main --model_type Transformer \
          --config config.yml --auto_config \
          train --with_eval

