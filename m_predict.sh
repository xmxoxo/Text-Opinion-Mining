#!/bin/bash 
#chkconfig: 2345 80 90
#description: 
#Author: xmxoxo
#update: 2019/8/28

echo 'start Predict...'

cd /mnt/sda1/transdat/bert-demo/Text-Opinion-Mining/Polarity/
sudo python run_Polarity.py --do_predict=true

cd /mnt/sda1/transdat/bert-demo/Text-Opinion-Mining/Category/
sudo python run_Category.py --do_predict=true
