#!/usr/bin/env python3
"""Encrypt a string"""

import argparse
import hashlib
import os
import sys


# colors
run = '\033[97m[~]\033[0m '
que = '\033[94m[?]\033[0m '
bad = '\033[91m[-]\033[0m '
info = '\033[93m[!]\033[0m '
good = '\033[92m[+]\033[0m '


def parse_args():

	parser = argparse.ArgumentParser()
	parser.add_argument('string', type=str, help='string to encrypt')
	parser.add_argument('-m', '--method', help='encryption method')
	parser.add_argument('-t', '--text', action='store_true', default=False, help='Save results to text file')
	parser.add_argument('--show_avail', action='store_true', default=False, help='Show algorithms available for you')
	parser.add_argument('--show_all', action='store_true', default=False, help='Show all algorithms')


	args = parser.parse_args()
	return args

def hasher(string, hash_type=None):
	hash_dict = {'Original String': string}
	try:
		if hash_type:
			hash_name = hash_type
			hash = getattr(hashlib, hash_type)
			hash_o = hash(string.encode())
			try:
				digested = hash_o.hexdigest()
			except TypeError:
				digested = hash_o.hexdigest(256)
			hash_dict.setdefault(hash_name, digested)

		else:
			all_hashes = hashlib.algorithms_guaranteed
			for hash in all_hashes:
				hash_name = hash
				hash = getattr(hashlib, hash)
				hash_o = hash(string.encode())

				try:
					digested = hash_o.hexdigest()
				except TypeError:
					print(hash_name)
					digested = hash_o.hexdigest(256)
					
				hash_dict.setdefault(hash_name, digested)
	except AttributeError as e:
		print(f'{bad}Encryption Unavailable: {hash_type}')
		print(f'{bad}Available Encryptions: {hashlib.algorithms_available}')
	return hash_dict

def show_avail():
	print(f'{info}Available Encryptions:')
	for hash in hashlib.algorithms_guaranteed:
		print(f'\t{hash}')

def show_all():
	print(f'{info}All Encryptions:')
	for hash in hashlib.algorithms_available:
		print(f'\t{hash}')


def save_to_txt(hash_dict):
	count = 0
	file = f'hashed_str_{count}.txt'
	while os.path.exists(file):
		count += 1
		file = f'hashed_str_{count}.txt'

	with open(file, 'w') as out:
		og_str = hash_dict['Original String']
		out.write(f'Original String:{og_str}')
		del hash_dict['Original String']

		for hash, hashed_str in hash_dict.items():
			out.write(f'{hash}:{hashed_str}\n')
	print(f'Results saved to {file}')

def main():
	args = parse_args()
	string = args.string
	hash_type = args.method

	if args.show_all:
		show_all()
		return

	if args.show_avail:
		show_avail()
		return

	hash_dict = hasher(string, hash_type)

	if args.text:
		save_to_txt(hash_dict)
		return
	else:
		og_str = hash_dict['Original String']
		print(f'{info}Original String --> {og_str}')
		del hash_dict['Original String']
		
		for hash, hashed_str in hash_dict.items():
			print(f'{good}{hash} --> {hashed_str}')


if __name__ == '__main__':
	main()
