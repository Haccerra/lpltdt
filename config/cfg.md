Configuration details used in the program.
This document can either be adjusted manually or through lpltdt --calib option.

CAMERA SETTINGS:
{
	camera_resolution_width=640
	camera_resolution_height=480
	camera_image_rotation_angle=0
	camera_recording_image_mode=STILL_IMAGE_MODE
	camera_time_between_taking_new_image=5
	camera_fps_to_be_captured_in_video_mode=5
}

LICENSE PLATE ALGORITHM SETTINGS:
{
	lpltdt_number_of_results_provided_by_alpr=1
	lpltdt_use_vehicle_classification_algorithm=NO
	lpltdt_default_country_locale_used_by_application=eu
	lpltdt_system_alpr_configuration_file_destination=/etc/openalpr/openalpr.con
	lpltdt_system_alpr_runtime_data_file_destination=/usr/share/openalpr/runtime_data
}
