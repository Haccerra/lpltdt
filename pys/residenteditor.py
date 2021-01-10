# GUI for changing residents database.


import sys
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from functools import partial


# Get system passed arguments.
try:
	absolute_path = sys.argv[1]
except Exception:
	print ("DEV MESSAGE: omnirun.sh did not provide proper argument for absolute program path.")
	exit (1)

try:
	input_argument = sys.argv[2]

	if ("--xterm" == input_argument):
		use_gui = False
	elif ("--gui" == input_argument):
		use_gui = True
	else:
		print ("Improper argument specified. Use --xterm for terminal based editing or --gui for database editing using GUI.")
		exit (1)

except Exception:
	# If no argument has been specified, assume GUI is in use.
	use_gui = True


# Join necessary directories.
sys.path.insert (0, "%s/pys"%absolute_path)
sys.path.insert (0, "%s/database"%absolute_path)
sys.path.insert (0, "%s/database/parser"%absolute_path)


# Import custom modules.
import DBResidentEditor as dbeditor


# @Brief: Function to create a GUI.
# @Input: None
# @Retrn: None
# @Throw: None
def gui_based_editing():

	# Create window.
	window = Tk ()
	window.title ("Residents database editor")
	window.geometry ("510x210")
	window.resizable (False, False)

	# Add window elements.
	residentname_label = Label (window, text = "Resident name: ", font = ("Arial Bold", 15))
	residentname_entrybox = Entry (window, width = 25)
	residentname_label.grid (column = 0, row = 0)
	residentname_entrybox.grid (column = 1, row = 0)

	residentsurname_label = Label (window, text = "Resident surname: ", font = ("Arial Bold", 15))
	residentsurname_entrybox = Entry (window, width = 25)
	residentsurname_label.grid (column = 0, row = 1)
	residentsurname_entrybox.grid (column = 1, row = 1)

	residentapartment_label = Label (window, text = "Apartment number: ", font = ("Arial Bold", 15))
	residentapartment_entrybox = Entry (window, width = 25)
	residentapartment_label.grid (column = 0, row = 2)
	residentapartment_entrybox.grid (column = 1, row = 2)

	residentcarmake_label = Label (window, text = "Car brand: ", font = ("Arial Bold", 15))
	residentcarmake_entrybox = Entry (window, width = 25)
	residentcarmake_label.grid (column = 0, row = 3)
	residentcarmake_entrybox.grid (column = 1, row = 3)

	residentcarmodel_label = Label (window, text = "Car model: ", font = ("Arial Bold", 15))
	residentcarmodel_entrybox = Entry (window, width = 25)
	residentcarmodel_label.grid (column = 0, row = 4)
	residentcarmodel_entrybox.grid (column = 1, row = 4)

	residentcarlicense_label = Label (window, text = "License plate: ", font = ("Arial Bold", 15))
	residentcarlicense_entrybox = Entry (window, width = 25)
	residentcarlicense_label.grid (column = 0, row = 5)
	residentcarlicense_entrybox.grid (column = 1, row = 5)


	# @Brief: Method for when button to load database is clicked.
	# @Input: None
	# @Retrn: None
	# @Throw: None
	def onclicklistener_loadresident():

		# Set new window style
		new_window = Toplevel (window)
		new_window.title ("Database")
		new_window.geometry ("510x270")
		new_window.resizable (False, False)

		# Add tabs
		tab = []
		tab_control = ttk.Notebook (new_window)

		try:

			db = dbeditor.DBResidentEditor(absolute_path + "/database/residents.db")
			dbdata = db.read()

			for id, data in enumerate (dbdata):
				new_tab = ttk.Frame (tab_control)
				tab.append (new_tab)

				tab_control.add (new_tab, text = "%s %s"%(data[dbeditor.RESIDENT_NAME], data[dbeditor.RESIDENT_SURNAME]))

				# Add window elements.
				residentname_label = Label (new_tab, text = "Resident name: ", font = ("Arial Bold", 15))
				residentname_entrybox = Entry (new_tab, width = 25, fg = "yellow")
				residentname_label.grid (column = 0, row = 0)
				residentname_entrybox.grid (column = 1, row = 0)

				residentsurname_label = Label (new_tab, text = "Resident surname: ", font = ("Arial Bold", 15))
				residentsurname_entrybox = Entry (new_tab, width = 25, state = "disabled")
				residentsurname_label.grid (column = 0, row = 1)
				residentsurname_entrybox.grid (column = 1, row = 1)

				residentapartment_label = Label (new_tab, text = "Apartment number: ", font = ("Arial Bold", 15))
				residentapartment_entrybox = Entry (new_tab, width = 25)
				residentapartment_label.grid (column = 0, row = 2)
				residentapartment_entrybox.grid (column = 1, row = 2)

				residentcarmake_label = Label (new_tab, text = "Car brand: ", font = ("Arial Bold", 15))
				residentcarmake_entrybox = Entry (new_tab, width = 25)
				residentcarmake_label.grid (column = 0, row = 3)
				residentcarmake_entrybox.grid (column = 1, row = 3)

				residentcarmodel_label = Label (new_tab, text = "Car model: ", font = ("Arial Bold", 15))
				residentcarmodel_entrybox = Entry (new_tab, width = 25)
				residentcarmodel_label.grid (column = 0, row = 4)
				residentcarmodel_entrybox.grid (column = 1, row = 4)

				residentcarlicense_label = Label (new_tab, text = "License plate: ", font = ("Arial Bold", 15))
				residentcarlicense_entrybox = Entry (new_tab, width = 25)
				residentcarlicense_label.grid (column = 0, row = 5)
				residentcarlicense_entrybox.grid (column = 1, row = 5)

				# Update fields.
				residentname_entrybox.configure (state = "normal")
				residentname_entrybox.insert (END, data[dbeditor.RESIDENT_NAME])
				
				residentsurname_entrybox.configure (state = "normal")
				residentsurname_entrybox.insert (END, data[dbeditor.RESIDENT_SURNAME])

				residentapartment_entrybox.configure (state = "normal")
				residentapartment_entrybox.insert (END, data[dbeditor.RESIDENT_APARTMENT])

				residentcarmake_entrybox.configure (state = "normal")
				residentcarmake_entrybox.insert (END, data[dbeditor.RESIDENT_CAR_BRAND])

				residentcarmodel_entrybox.configure (state = "normal")
				residentcarmodel_entrybox.insert (END, data[dbeditor.RESIDENT_CAR_MODEL])

				residentcarlicense_entrybox.configure (state = "normal")
				residentcarlicense_entrybox.insert (END, data[dbeditor.RESIDENT_CAR_LICENSE])

				# Make fields uneditable.
				residentname_entrybox.configure (state = "disabled")
				residentsurname_entrybox.configure (state = "disabled")
				residentapartment_entrybox.configure (state = "disabled")
				residentcarmake_entrybox.configure (state = "disabled")
				residentcarmodel_entrybox.configure (state = "disabled")
				residentcarlicense_entrybox.configure (state = "disabled")


				# @Brief: Remove specific entry.
				# @Input: license_plate - unique identifier for each button
				# @Retrn: None
				# @Throw: None
				def onclicklistener_remove_entry(license_plate):
					db.remove(license_plate)
					new_window.destroy ()
					onclicklistener_loadresident()


				remove_entry_button = Button (new_tab, width = 25, text = "Remove Entry", bg = "black", fg = "yellow", command = partial (onclicklistener_remove_entry, data[dbeditor.RESIDENT_CAR_LICENSE]))
				remove_entry_button.grid (column = 1, row = 7)

				tab_control.pack (expand = 1, fill = "both")

		except Exception:
			messagebox.showerror ("Error", "Could not load database")


	loadresidents_button = Button (window, width = 25, text = "Load", bg = "black", fg = "yellow", command = onclicklistener_loadresident)
	loadresidents_button.grid (column = 0, row = 7)


	# @Brief: Add new resident data to the database
	# @Input: None
	# @Retrn: None
	# @Throw: None
	def onclicklistener_addnewresident():
		db = dbeditor.DBResidentEditor(absolute_path + "/database/residents.db")

		append_data = [ 							\
					residentname_entrybox.get (),			\
					residentsurname_entrybox.get (),		\
					residentapartment_entrybox.get (),		\
					residentcarmake_entrybox.get (),		\
					residentcarmodel_entrybox.get (),		\
					residentcarlicense_entrybox.get ()		\
			      ]
		try:
			db.append(append_data)
			messagebox.showinfo ("Success", "New resident added.")

		except Exception:
			messagebox.showerror ("Error", "NEW RESIDENT COULD NOT BE ADDED!")

		residentname_entrybox.delete (0, END)
		residentsurname_entrybox.delete (0, END)
		residentapartment_entrybox.delete (0, END)
		residentcarmake_entrybox.delete (0, END)
		residentcarmodel_entrybox.delete (0, END)
		residentcarlicense_entrybox.delete (0, END)
		

	addnewresident_button = Button (window, width = 25, text = "Add", bg = "black", fg = "yellow", command = onclicklistener_addnewresident)
	addnewresident_button.grid (column = 1, row = 7)


	window.mainloop ()


# @Brief: Not planned to be implemented.
# @Input: None
# @Retrn: None
# @Throw: None
def term_based_editing():
	pass


# Independent part of the program. Used to update residents list data.
if ("__main__" == __name__):

	# Use GUI based editing.
	if (False != use_gui):
		gui_based_editing()

	# Use terminal based editing.
	else:
		term_based_editing()

