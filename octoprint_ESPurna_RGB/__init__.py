# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin
import requests
import re

class ESPurna_RGBPlugin(octoprint.plugin.StartupPlugin,
							octoprint.plugin.TemplatePlugin,
							octoprint.plugin.SettingsPlugin):
	def on_after_startup(self):
		self._logger.info("Espruna booted")

	def on_settings_load(self):
		data = octoprint.plugin.SettingsPlugin.on_settings_load(self)
		return data

	def on_settings_save(self, data):
		octoprint.plugin.SettingsPlugin.on_settings_save(self, data)

	def get_settings_defaults(self):
		return dict(
			url="http://0.0.0.0",
			key="key"
		)

	def get_template_configs(self):
		return [
			dict(type="settings", name="Espruna LED Settings", custom_bindings=False)
		]

	def handle_M150(self, comm_instance, phase, cmd, cmd_type, gcode, *args, **kwargs):
		if gcode and cmd.startswith ("M150"):
			rgb = {'r':0, 'g':0, 'b':0}
			for match in re.finditer(r'([RGUBrgub]) *(\d*)', cmd):
				k = match.group(1).lower()
				if k == 'u': k = 'g'
				try:
					val = int(match.group(2))
				except ValueError:
					val = 255
				val = max(min(val, 255), 0)
				rgb[k] = val
			hex = "#{:02x}{:02x}{:02x}".format(rgb['r'], rgb['g'], rgb['b'])
			self._logger.debug(u"Hex: %s" % (hex,))
			try:
				if hex == '#000000':
					#disable the led relay
					requests.put("%s/api/relay/0" % self._settings.get(['url']),
						data={'apikey': self._settings.get(['key']), 'value': '0'})
				else:
					#enable the led relay
					requests.put("%s/api/relay/0" % self._settings.get(['url']),
					   data={'apikey': self._settings.get(['key']), 'value': '1'})
					#pass hex color value using the color api
					requests.put("%s/api/color" % self._settings.get(['url']),
					   data={'apikey': self._settings.get(['key']), 'value': hex})
			except:
				self._logger.debug("Bad request")
			return None,

	def get_update_information(self):
		return dict(
			espurna_rgb=dict(
				displayName="Espurna RGB Plugin",
				displayVersion=self._plugin_version,

				# version check: github repository
				type="github_release",
				user="pokeimon",
				repo="OctoPrint-ESPurnaRGB",
				current=self._plugin_version,

				# update method: pip
				pip="https://github.com/pokeimon/OctoPrint-ESPurnaRGB/archive/{target_version}.zip"
			)
		)

__plugin_name__ = "Espurna RGB"

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = ESPurna_RGBPlugin()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.comm.protocol.gcode.queuing": __plugin_implementation__.handle_M150,
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
	}