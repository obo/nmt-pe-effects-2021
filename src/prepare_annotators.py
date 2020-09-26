#!/usr/bin/env python3

import argparse
from random import shuffle
from glob import glob
from os import makedirs

parser = argparse.ArgumentParser(
    description='Shuffle documents for annotators in NMT-PE-Effects.')
parser.add_argument('docs_dir',
                    help='Path to the root document directory')
parser.add_argument('out_dir',
                    help='Path to the output directory (doesn\'t have to exist)')
parser.add_argument('-s', '--shuffle-order',
                    default=False, action='store_true', help='Shuffle base order')
parser.add_argument('-d', '--shuffle-order-annotator',
                    default=False, action='store_true', help='Shuffle order for every annotator')
args = parser.parse_args()

mt_order = ['mt1', 'mt2', 'mt3']
mt_number = len(mt_order)
# doc_order = ['hole', 'whistle', 'china', 'turner',
#              'leap', 'lease', 'audit_i', 'audit_r']
doc_order = ['hole', 'whistle', 'china']

print('Creating annotator queues')

shuffle(mt_order)
if args.shuffle_order:
    shuffle(doc_order)

mt_buckets = [{} for _ in range(mt_number)]

for doc_name in doc_order:
    for mt_index, mt_name in enumerate(mt_order):
        filename = f'{args.docs_dir}/{doc_name}-{mt_name}'
        with open(filename, 'r') as f:
            data = f.read()
            mt_buckets[mt_index][doc_name] = data

annotator_buckets = [{} for _ in range(mt_number)]

offset = 0
for doc_name in doc_order:
    for mt_index, mt_name in enumerate(mt_order):
        annotator_index = (mt_index + offset) % mt_number
        annotator_buckets[annotator_index][doc_name] = mt_buckets[mt_index][doc_name]
    offset = (offset+1) % mt_number


print('Serializing data')

annotator_serial = [""] * mt_number

for annotator_index, annotator_bucket in enumerate(annotator_buckets):
    for doc_name in doc_order:
        annotator_serial[annotator_index] += annotator_buckets[annotator_index][doc_name]

print('Storing data')

makedirs(args.out_dir, exist_ok=True)
for annotator_index, annotator_bucket in enumerate(annotator_buckets):
    with open(f'{args.out_dir}/a{annotator_index}', 'w') as f:
        f.write(annotator_serial[annotator_index])
