# coding=utf-8
from __future__ import absolute_import
import math

### (Don't forget to remove me)
# This is a basic skeleton for your plugin's __init__.py. You probably want to adjust the class name of your plugin
# as well as the plugin mixins it's subclassing from. This is really just a basic skeleton to get you started,
# defining your plugin as a template plugin, settings and asset plugin. Feel free to add or remove mixins
# as necessary.
#
# Take a look at the documentation on what other plugin mixins are available.

import octoprint.plugin


class Octoprint_filament_progressPlugin(octoprint.plugin.SettingsPlugin, octoprint.plugin.AssetPlugin,
                                        octoprint.plugin.TemplatePlugin, octoprint.plugin.StartupPlugin):
    extrudedLength = 0
    lastLength = 0
    lastDelta = 0
    isAbsolute = True

    def on_after_startup(self):
        self._logger.info("Wir leben!")
        self._logger.info("Wir leben!")
        self._logger.info("Wir leben!")
        self._logger.info("Wir leben!")
        self._logger.info("Wir leben!")
        self._logger.info("Wir leben!")
        self._logger.info("Wir leben!")

    def filament_odometer(self, comm_instance, phase, cmd, cmd_type, gcode, *args, **kwargs):
        # self._logger.info("Comm_instance: " + comm_instance)
        # self._logger.info("Phase: " + phase)
        # self._logger.info("Cmd: " + cmd)
        # self._logger.info("Gcode: " + gcode)

        if "G91" == gcode:  # G91 -> Relative Mode.
            self.isAbsolute = False
            return
        if "G90" == gcode:  # G90 -> Absolute Mode.
            self.isAbsolute = True
            return
        if "G0" == gcode or "G1" == gcode or "G2" == gcode or "G3" == gcode:  # G0,1,2,3 -> Movements.
            value = self._getCode(cmd, "E", float)
            if value is not None:
                if self.isAbsolute:
                    self.lastDelta = value - self.lastLength
                    self.extrudedLength += self.lastDelta
                    self.lastLength = value
                else:
                    self.lastDelta = value
                    self.extrudedLength += self.lastDelta
                    self.lastLength += value
                self._logger.info("Sum Distance: " + self.extrudedLength.__str__())
            return
        if "G92" == gcode:  # G92 -> Reset lastLength to the given value.
            self.lastLength = self._getCode(cmd, "E", float)
            return
        if "G9999" == gcode:
            self._logger.info("Total amount extruded: " + self.extrudedLength.__str__())

    def _getCode(self, line, code, c):
        n = line.find(code) + 1
        if n < 1:
            return None
        m = line.find(" ", n)
        try:
            if m < 0:
                result = c(line[n:])
            else:
                result = c(line[n:m])
        except ValueError:
            return None

        if math.isnan(result) or math.isinf(result):
            return None

        return result

    ##~~ SettingsPlugin mixin

    def get_settings_defaults(self):
        return dict(
            # put your plugin's default settings here
        )

    ##~~ AssetPlugin mixin

    def get_assets(self):
        # Define your plugin's asset files to automatically include in the
        # core UI here.
        return dict(
            js=["js/octoprint-filament-progress.js"],
            css=["css/octoprint-filament-progress.css"],
            less=["less/octoprint-filament-progress.less"]
        )

    ##~~ Softwareupdate hook

    def get_update_information(self):
        # Define the configuration for your plugin to use with the Software Update
        # Plugin here. See https://docs.octoprint.org/en/master/bundledplugins/softwareupdate.html
        # for details.
        return dict(
            octoprint_filament_progress=dict(
                displayName="Octoprint-filament-progress Plugin",
                displayVersion=self._plugin_version,

                # version check: github repository
                type="github_release",
                user="DJGummikuh",
                repo="octoprint-filament-progress",
                current=self._plugin_version,

                # update method: pip
                pip="https://github.com/DJGummikuh/octoprint-filament-progress/archive/{target_version}.zip"
            )
        )


# If you want your plugin to be registered within OctoPrint under a different name than what you defined in setup.py
# ("OctoPrint-PluginSkeleton"), you may define that here. Same goes for the other metadata derived from setup.py that
# can be overwritten via __plugin_xyz__ control properties. See the documentation for that.
__plugin_name__ = "Octoprint-filament-progress Plugin"

# Starting with OctoPrint 1.4.0 OctoPrint will also support to run under Python 3 in addition to the deprecated
# Python 2. New plugins should make sure to run under both versions for now. Uncomment one of the following
# compatibility flags according to what Python versions your plugin supports!
# __plugin_pythoncompat__ = ">=2.7,<3" # only python 2
# __plugin_pythoncompat__ = ">=3,<4" # only python 3
__plugin_pythoncompat__ = ">=2.7,<4"  # python 2 and 3


def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = Octoprint_filament_progressPlugin()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information,
        "octoprint.comm.protocol.gcode.sent": __plugin_implementation__.filament_odometer
    }
