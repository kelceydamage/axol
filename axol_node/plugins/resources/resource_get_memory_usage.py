#! /usr/bin/env python
#-----------------------------------------#
#Copyright [2015] [Kelcey Jamison-Damage]

#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#You may obtain a copy of the License at

#    http://www.apache.org/licenses/LICENSE-2.0

#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.

# Imports
#-----------------------------------------------------------------------#
from axol_common.classes.common_logger import CommonLogger
from axol_common.classes.common_data_object import GenericDataObject
from axol_common.classes.common_resource import CommonResource
from axol_common.classes.common_math import CommonMath
from axol_common.database.cassandra_wrapper import insert
from classes.axol_resource import AxolResource
from axol_config import api
from aapi.aapi import app as app
from flask import jsonify
from flask import request

class ResourceGetMemoryUsage(AxolResource):
	"""docstring for ResourceGetProcessorUsage
	Must implement:
		_show_help()
		self.source = {keyword}
		self.local = Bool
		self.store = Bool
		self.profiler = Bool
		api_<name of your api>()
		calculate_new_fields()
		write_to_database()
	Optional:
		if self.store = True, write_to_database() function must be implemented
	"""
	required_post = {
		'role': (True, u's'),
		'profile': (False, u's')
		}

	def __init__(self):
		super(ResourceGetMemoryUsage, self).__init__()
		self.source = 'memory'
		self.local = False
		self.store = True
		self.profiler = True

	def _show_help(self):
		return {
			'help': {
				'api': '/api/get_memory_usage',
				'method': 'POST',
				'required_data': {
					'role': '<some role>',
					'alert_type': ['email', 'text']
					},
				'version': api
				}
			}

	@staticmethod
	@app.route('/api/get_memory_usage', methods=['GET', 'POST'])
	def api_get_memory_usage():
		if request.method == 'GET':
			return jsonify(ResourceGetMemoryUsage()._show_help())
		try:
			data = CommonResource.handle_request(
				request=request,
				params=ResourceGetMemoryUsage.required_post
				)
		except Exception, e:
			report = CommonLogger.log(
				error=e,
				source='get_memory_usage',
				method='api_get_memory_usage'
				)
			return jsonify(report)
		try:
			response = ResourceGetMemoryUsage().create_async_job(
				data=data
				)
		except Exception, e:
			report = CommonLogger.log(
				error=e,
				source='get_memory_usage',
				method='api_get_memory_usage'
				)
			return jsonify(report)
		return jsonify(response)

	def calculate_new_fields(self, response_object):
		def calculate_current_usage(response_object):
			n = float(response_object.memused) / 1000
			n = int(n) + 0
			response_object.current_usage = n
			return response_object

		def calculate_usage_for_health(response_object):
			response_object.normalized_indicator = (
				float(response_object.memused) / float(response_object.memtotal)
				) / 1 + 0
			response_object.multiplier = 1
			response_object.threshold_red = 90
			response_object.scale = response_object.memtotal / 200000
			return response_object

		if response_object.error == None:
			response_object = calculate_usage_for_health(
				response_object=response_object
				)
			response_object = calculate_current_usage(
				response_object=response_object
				)
			response_object.health_indicator = CommonMath.adaptive_filtration(
				normalized_indicator=response_object.normalized_indicator,
				multiplier=response_object.multiplier,
				threshold_red=response_object.threshold_red,
				scale=response_object.scale
				)
			self.threshold_validation(response_object)
		return response_object

	def post_processing(self, axol_task_value):
		clusters = {'api': [], 'web': []}
		try:
			clusters = CommonMath.derive_clusters(
				clusters=clusters,
				map_value='current_usage',
				axol_task_value=axol_task_value
				)
		except Exception, e:
			print 'ERROR POST-PROC: %s' % e
		try:
			for cluster in clusters:
				clusters[cluster] = CommonMath.map_deviation(
					integer_list=clusters[cluster]
				)
				clusters[cluster]['source'] = self.source
				clusters[cluster]['name'] = cluster
		except Exception, e:
			print 'ERROR POST-PROC 2: %s' % e
		try:
			self.query([
				insert(
					data_object=clusters,
					table_space='axol_metrics.clusters'
					)]
				)
		except Exception, e:
			print 'ERROR POST-PROC 3: %s' % e
		return axol_task_value

	def write_to_database(self, axol_task_value):
		self.query([
			insert(
				data_object=axol_task_value,
				table_space='axol_metrics.memory_usage'
				)]
			)

