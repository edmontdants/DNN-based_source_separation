#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import torch
import torch.nn as nn

from utils.utils import set_seed
from dataset import SpectrogramTrainDataset, TrainDataLoader
from driver import Trainer

parser = argparse.ArgumentParser(description="Training of ADANet")

parser.add_argument('--wav_root', type=str, default=None, help='Path for dataset ROOT directory')
parser.add_argument('--train_json_path', type=str, default=None, help='Path for train.json')
parser.add_argument('--valid_json_path', type=str, default=None, help='Path for valid.json')
parser.add_argument('--sr', type=int, default=10, help='Sampling rate')
parser.add_argument('--window_fn', type=str, default='hamming', help='Window function')
# Model configuration
parser.add_argument('--n_sources', type=int, default=None, help='# speakers')
parser.add_argument('--criterion', type=str, default='sisdr', choices=['sisdr'], help='Criterion')
parser.add_argument('--optimizer', type=str, default='adam', choices=['sgd', 'adam'], help='Optimizer, [sgd, adam]')
parser.add_argument('--lr', type=float, default=0.001, help='Learning rate. Default: 0.001')
parser.add_argument('--weight_decay', type=float, default=0, help='Weight decay (L2 penalty). Default: 0')
parser.add_argument('--max_norm', type=float, default=None, help='Gradient clipping')

parser.add_argument('--batch_size', type=int, default=4, help='Batch size. Default: 128')
parser.add_argument('--epochs', type=int, default=5, help='Number of epochs')
parser.add_argument('--model_dir', type=str, default='./tmp/model', help='Model directory')
parser.add_argument('--loss_dir', type=str, default='./tmp/loss', help='Loss directory')
parser.add_argument('--sample_dir', type=str, default='./tmp/sample', help='Sample directory')
parser.add_argument('--continue_from', type=str, default=None, help='Resume training')
parser.add_argument('--use_cuda', type=int, default=1, help='0: Not use cuda, 1: Use cuda')
parser.add_argument('--overwrite', type=int, default=0, help='0: NOT overwrite, 1: FORCE overwrite')
parser.add_argument('--seed', type=int, default=42, help='Random seed')

def main(args):
    set_seed(args.seed)
    
    loader = {}
    
    train_dataset = SpectrogramTrainDataset(args.wav_root, args.train_json_path)
    valid_dataset = SpectrogramTrainDataset(args.wav_root, args.valid_json_path)
    print("Training dataset includes {} samples.".format(len(train_dataset)))
    print("Valid dataset includes {} samples.".format(len(valid_dataset)))
    
    loader['train'] = TrainDataLoader(train_dataset, batch_size=args.batch_size, shuffle=True)
    loader['valid'] = TrainDataLoader(valid_dataset, batch_size=args.batch_size, shuffle=False)
    
    for mixture, sources in loader['train']:
        print(mixture.size(), sources.size())
        raise ValueError("Stop")
    
    if args.use_cuda:
        if torch.cuda.is_available():
            model.cuda()
            model = nn.DataParallel(model)
            print("Use CUDA")
        else:
            raise ValueError("Cannot use CUDA.")
    else:
        print("Does NOT use CUDA")
    
