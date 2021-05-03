import requests
import argparse
from datetime import datetime
from pprint import pprint

# Base URL
COVIN_BASE_URL = "https://cdn-api.co-vin.in/api/v2"

# Get list of states
STATES = "/admin/location/states"
DISTRICTS = "/admin/location/districts/{state_id}"
CALENDER_BY_DISTRICT = "/appointment/sessions/public/calendarByDistrict"
CALENDER_BY_PIN = "/appointment/sessions/public/calendarByPin"

DATE = datetime.today().strftime("%d-%m-%Y")
DEFAULT_AGE_LIMIT = 18

states = {
	"states": []
}

districts = {
	"districts": []
}

centers = {
	"centers": []
}

search_types = {
	"PIN": "pin",
	"DISTRICT": "district",
}

def define_arguments(parser):
	# State
	parser.add_argument(
		"-t",
		"--search_type",
		help="The type of search to perform. You can either directly give a pincode or give a combination of state + district.",
		type=str,
		default=search_types["DISTRICT"],
		choices=[
			search_types["PIN"],
			search_types["DISTRICT"],
		]
	)
	# State
	parser.add_argument(
		"-s",
		"--state",
		help="The name of the state",
		type=str,
		default=None
	)
	# District
	parser.add_argument(
		"-d",
		"--district",
		help="The name of the district",
		type=str,
		default=None
	)
	# Age limit
	parser.add_argument(
		"-a",
		"--age_limit",
		help="The age limit. Put as 18 for 18+ and 45 for 45+.",
		type=int,
		default=DEFAULT_AGE_LIMIT
	)
	# Pincode
	parser.add_argument(
		"-p",
		"--pin_code",
		help="The pin code. Use this option with search_type = pin.",
		type=int,
		default=None
	)

def get_states():
	global states
	states_response = requests.get(
		COVIN_BASE_URL + STATES
	)
	if states_response.status_code == 200:
		states = states_response.json()

def get_districts(state_id):
	global districts
	districts_response = requests.get(
		COVIN_BASE_URL + DISTRICTS.format(state_id=state_id)
	)
	if districts_response.status_code == 200:
		districts = districts_response.json()

def get_centers(search_type, params):
	path = CALENDER_BY_DISTRICT
	if search_type == search_types["PIN"]:
		path = CALENDER_BY_PIN
	centers_response = requests.get(
		COVIN_BASE_URL + path,
		params=params
	)
	if centers_response.status_code == 200:
		return centers_response.json()
	else:
		return centers

def find_closest_state(search_state):
	for state in states["states"]:
		# TODO: Find closest search. DP FTW.
		if state["state_name"] == search_state:
			return state["state_id"], state["state_name"]
	return None

def find_closest_district(search_district):
	for district in districts["districts"]:
		if district["district_name"] == search_district:
			return district["district_id"], district["district_name"]
	return None

def search_by_district(state, district):
	get_states()

	if state == None:
		print("Select a state: ", end="")
		state = input()

	state_id, state_name = find_closest_state(state)

	print("State Id: {state_id}, State Name: {state_name} ".format(state_id=state_id, state_name=state_name))

	get_districts(state_id)

	if district == None:
		print("Select a district: ", end="")
		district = input()

	district_id, district_name = find_closest_district(district)

	print("District Id: {district_id}, District Name: {district_name} ".format(district_id=district_id, district_name=district_name))

	return {
		"date": DATE,
		"district_id": district_id,
	}

def search_by_pincode(pin_code):
	print ("Pin Code is: ", pin_code)
	return {
		"date": DATE,
		"pincode": pin_code,
	}

def print_available_sessions(available_sessions):
	if len(available_sessions) == 0:
		print("No available sessions!!")
	else:
		print("Available sessions are: ")
		row_template = "{:>30}" * 3
		print(row_template.format(
			"name", "pincode", "date"
		))
	for center, session in available_sessions:
		print(
			row_template.format(
				center["name"], center["pincode"], session["date"]
			)
		)

if __name__ == "__main__":
	# Init the arg parser
	parser = argparse.ArgumentParser()
	# Defining all the arguments
	define_arguments(parser)
	# Extracting all the arguments
	args = parser.parse_args()
	
	search_type = args.search_type
	state = args.state
	district = args.district
	age_limit = args.age_limit
	pin_code = args.pin_code

	params = {}
	if search_type == search_types["DISTRICT"]:
		params = search_by_district(state, district)
	else:
		params = search_by_pincode(pin_code)

	centers = get_centers(search_type, params)

	available_sessions = []

	for center in centers["centers"]:
		for session in center["sessions"]:
			if session["min_age_limit"] == age_limit and session["available_capacity"] > 0:
				available_sessions.append((center, session))
	print_available_sessions(
		available_sessions
	)
	
		

