import hashlib
import json
from textwrap import dedent
from uuid import uuid4
import jsonpickle
from flask import Flask
from urllib.parse import urlparse
from Crypto.PublicKey import RSA
from Crypto.Signature import *
from time import time
from datetime import datetime
import requests


class Blockchain (object):
	def __init__(self):
		self.chain = [self.addGenesisBlock()];
		self.pendingTransactions = [];
		self.difficulty = 2;
		self.minerRewards = 50;
		self.blockSize = 10;
		self.nodes = set();

	def register_node(self, address):
		parsedUrl = urlparse(address)
		self.nodes.add(parsedUrl.netloc)

	def resolveConflicts(self):
		neighbors = self.nodes;
		newChain = None;

		maxLength = len(self.chain);

		for node in neighbors:
			response = requests.get(f'http://{node}/chain');

			if response.status_code == 200:
				length = response.json()['length'];
				chain = response.json()['chain'];

				if length > maxLength and self.isValidChain():
					maxLength = length;
					newChain = chain;

		if newChain:
			self.chain = self.chainJSONdecode(newChain);
			print(self.chain);
			return True;

		return False;
