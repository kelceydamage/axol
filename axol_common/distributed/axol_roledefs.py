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

import boto.ec2
import re

def generate_base_roles(application_flag='internal'):
	# Application flag can be either internal or external
	#application_flag = 'external'
	#application_flag = 'internal'

	def ec2_get_all_instances():
		ec2 = boto.ec2.connect_to_region(
			"us-west-2",
			aws_access_key_id="ACCESS-KEY",
			aws_secret_access_key="SECRET-KEY",
			)

		ec2_instance_list = ec2.get_all_instances()
		return ec2_instance_list

	def generate_roledefs(ec2_instance_list):
		roledefs = {}
		local_instance_list = []

		for item in ec2_instance_list:
			local_instance_list.append(item.instances[0])

		for item in local_instance_list:
			if str(item._state) == 'running(16)':
				roledefs[item.tags['Name']] = {}
				roledefs[item.tags['Name']]['internal'] = item.private_ip_address
				roledefs[item.tags['Name']]['external'] = item.ip_address

		return roledefs

	# Filter IP addresses into a role collection
	def generate_role(_list, _filter, application_flag):
		for role in roledefs:
			if re.search(r'%s.*' % _filter, role) \
			and not re.search(r'.*all.*', role) \
			or re.search(r'.*servers.*', role):
				try:
					_list.append(
						roledefs[role][application_flag]
						)
				except Exception, e:
					pass

		return _list

	roledefs = generate_roledefs(ec2_get_all_instances())

	roledefs['dev_axol_node'] = {
		'internal': '10.100.10.63',
		'external': '10.100.10.63'
		}

	roledefs['dev_axol_scheduler'] = {
		'internal': '10.100.10.59',
		'external': '10.100.10.59'
		}

	# Create a role for all mysql read slaves
	mysql_read_slaves = []
	roledefs['mysql_read_slaves'] = generate_role(
		mysql_read_slaves,
		'hq_db_slave_dashboard',
		application_flag
		)

	# Create a role for all mysql servers
	mysql_servers = []
	roledefs['mysql_servers'] = generate_role(
		mysql_servers,
		'live.*db',
		application_flag
		)

	# Create a role for all production marketing servers
	marketing_servers = []
	roledefs['marketing_servers'] = generate_role(
		marketing_servers,
		'marketing',
		application_flag
		)

	# Create a role for all production servers
	production_servers = []
	roledefs['production_servers'] = generate_role(
		production_servers,
		'live',
		application_flag
		)

	# Create a role for all staging application servers
	staging_api_servers = []
	roledefs['staging_api_servers'] = generate_role(
		staging_api_servers,
		'staging_api',
		application_flag
		)

	# Create a role for all production application servers
	hq_api_servers = []
	roledefs['hq_api_servers'] = generate_role(
		hq_api_servers,
		'hq_api',
		application_flag
		)

	# Create a role for all production nfs servers
	hq_nfs_servers = []
	roledefs['hq_nfs_servers'] = generate_role(
		hq_nfs_servers,
		'hq_nfs',
		application_flag
		)

	# Create a role for all production web servers
	hq_web_servers = []
	roledefs['hq_web_servers'] = generate_role(
		hq_web_servers,
		'hq_web',
		application_flag
		)

	# Create a role for all production mysql servers
	hq_mysql_servers = []
	roledefs['hq_mysql_servers'] = generate_role(
		hq_mysql_servers,
		'hq_db',
		application_flag
		)

	# Create a role for all staging mysql slave servers
	staging_mysql_servers = []
	roledefs['staging_mysql_servers'] = generate_role(
		staging_mysql_servers,
		'staging_db',
		application_flag
		)

	# Create a role for all staging web servers
	staging_web_servers = []
	roledefs['staging_web_servers'] = generate_role(
		staging_web_servers,
		'staging_web',
		application_flag
		)

	# Create a role for all staging nfs servers
	staging_nfs_servers = []
	roledefs['staging_nfs_servers'] = generate_role(
		staging_nfs_servers,
		'staging_nfs',
		application_flag
		)

	# Create a role for all staging servers
	staging_all = []
	roledefs['staging_all'] = generate_role(
		staging_all,
		'staging',
		application_flag
		)

	# Create a role for all production servers
	hq_all = []
	roledefs['hq_all'] = generate_role(
		hq_all,
		'live_hq',
		application_flag
		)

	# Create a role for all servers
	do_not_use_all = []
	roledefs['do_not_use_all'] = generate_role(
		do_not_use_all,
		'',
		application_flag
		)

	# Create a role for local server debugging
	local_debug = []
	roledefs['local_debug'] = ['127.0.0.1']

	# Create a role for custom health monitoring
	heartbeat = []
	roledefs['heartbeat'] = generate_role(
		heartbeat,
		'_L',
		application_flag
		)

	# Create a role for testing
	debug = []
	roledefs['debug'] = generate_role(
		debug,
		'staging_web_1_L',
		application_flag
		)

	roledefs['axol'] = [
		'10.100.10.63',
		'10.100.10.59'
		]

	elasticsearch = []
	roledefs['staging_elasticsearch'] = generate_role(
		elasticsearch,
		'staging_elasticsearch',
		application_flag
		)

	return roledefs

#roledefs = generate_base_roles('internal')
#roledefs = generate_base_roles('external')
roledefs = {'temp': ['','']}
print roledefs



