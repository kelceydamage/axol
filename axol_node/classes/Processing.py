#! /usr/bin/env python
#-----------------------------------------#
# Copyright [2015] [Kelcey Jamison-Damage]

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#    http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Imports
#-----------------------------------------------------------------------#

import sys, os, time
import time
from random import randint
from multiprocessing import Process, Pool, Queue

# Processing Class
#-----------------------------------------------------------------------#


class Processing(object):
	"""docstring for Processing"""
	def __init__(self):
		super(Processing, self).__init__()
		pass

# Processing wrapper methods
#-----------------------------------------------------------------------#

	def create_queue(self):
		queue = Queue()
		return queue

	def generate_pool(self, processes=4):
		pool = Pool(processes)
		return pool

	def new_process_pool(self, pool, func, data):
		result = pool.apply_async(func, data)
		return result

	def new_process(self, func, data):
		process = Process(target=func, args=data)
		process.start()
		return process

	def new_process_map(self, pool, func, data, data2='', data3=''):
		result = pool.map(func, [data])
		return result

