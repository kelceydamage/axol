#! /usr/bin/env python
#-----------------------------------------#
# Written by Kelcey Damage, 2013

# Imports
#-----------------------------------------------------------------------#
from axol_common.classes.common_logger import CommonLogger
from axol_common.classes.common_data_object import GenericDataObject
from axol_common.classes.common_resource import CommonResource
from axol_common.distributed.axol_roledefs import generate_base_roles
from classes.axol_resource import AxolResource
from axol_config import api
from aapi.aapi import app as app
from flask import jsonify
from flask import request

class ResourceGetAllRoles(AxolResource):
	"""docstring for ResourceGetAllRoles
	Must implement:
		_show_help
		self.methods = {<method_type>: function}
		self.source = {keyword}
		request_{keyword}_api
		calculate_new_fields
	"""
	required_post = {
		'network': (True, u's'),
		'profile': (False, u's')
		}

	def __init__(self):
		super(ResourceGetAllRoles, self).__init__()
		self.source = 'get_all_roles'
		self.local = True

	def _show_help(self):
		return {
			'Help': {
				'api': '/api/get_all_roles',
				'method': 'POST',
				'required data': {
					'network': '<internal, external>'
					},
				'version': api
				}
			}

	@staticmethod
	@app.route('/api/get_all_roles', methods=['POST', 'GET'])
	def api_get_all_roles():
		if request.method == 'GET':
			return jsonify(ResourceGetAllRoles()._show_help())
		try:
			data = CommonResource.handle_request(request, ResourceGetAllRoles.required_post)
		except Exception, e:
			CommonLogger.log(e, 'get_all_roles', 'api_get_all_roles')
			return jsonify({'response': {'error': str(e)}})
		try:
			roledefs = generate_base_roles(data.network)
		except Exception, e:
			CommonLogger.log(e, 'get_all_roles', 'api_get_all_roles')
			return jsonify({'response': {'error': str(e)}})
		return jsonify({'response': roledefs})
