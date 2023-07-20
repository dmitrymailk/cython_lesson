export TASK_NAME=cola
export CUDA_VISIBLE_DEVICES=2

# python cython_glue_wrapper.py \
# python -m cProfile -s cumulative python_glue.py \
# python -m cProfile -o profile.prof python_glue.py \
python python_glue.py \
  --model_name_or_path bert-base-cased \
  --task_name $TASK_NAME \
  --do_train \
  --do_eval \
  --max_seq_length 128 \
  --per_device_train_batch_size 32 \
  --learning_rate 2e-5 \
  --num_train_epochs 3 \
  --output_dir ./ignore/$TASK_NAME/ \
  --overwrite_output_dir


# default script, Python 3.10.9, A100 
# ***** train metrics *****
#   epoch                    =        3.0
#   train_loss               =     0.3427
#   train_runtime            = 0:02:30.89
#   train_samples            =       8551
#   train_samples_per_second =    170.001
#   train_steps_per_second   =      5.328
# ***** eval metrics *****
#   epoch                     =        3.0
#   eval_loss                 =     0.5144
#   eval_matthews_correlation =     0.5754
#   eval_runtime              = 0:00:02.16
#   eval_samples              =       1043
#   eval_samples_per_second   =    481.356
#   eval_steps_per_second     =     60.458

# default script, Python 3.10.9 +  default Cython, A100
# ***** train metrics *****
#   epoch                    =        3.0
#   train_loss               =     0.3427
#   train_runtime            = 0:02:28.38
#   train_samples            =       8551
#   train_samples_per_second =    172.877
#   train_steps_per_second   =      5.418
# ***** eval metrics *****
#   epoch                     =        3.0
#   eval_loss                 =     0.5144
#   eval_matthews_correlation =     0.5754
#   eval_runtime              = 0:00:02.17
#   eval_samples              =       1043
#   eval_samples_per_second   =    479.472
#   eval_steps_per_second     =     60.221