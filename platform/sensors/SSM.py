# Sound Sensor Module.


import RPi.GPIO as gio


LOW     = 0
HIGH    = 1
UNKNOWN = 2


gio_status = UNKNOWN


# @Brief:
# @Attrb:
# @Throw:
def configure_sound_sensor(gio_pin = 17):

	gio.setmode (gio.BCM)
	gio.setup (gio_pin, gio.IN)

	def callback_function(gio_pin):
		global gio_status

		if (gio.input (gio_pin)):
			gio_status = LOW
		else:
			gio_status = HIGH

	gio.add_event_detect (gio_pin, gio.BOTH, bouncetime = 300)
	gio.add_event_callback (gio_pin, callback_function)

def get_sound_sensor_gio(gio_pin = 17):
	return gio.input (gio_pin)
