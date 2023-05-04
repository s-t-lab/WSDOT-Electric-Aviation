from re import sub

def snake_case(s):
    return '_'.join(
        sub('([A-Z][a-z]+)', r' \1',
        sub('([A-Z]+)', r' \1',
        s.replace('-', ' '))).split()).lower()

def get_label(airport, operation_category_short, ops_scenario, feasibility_scenario, adoption_scenario):
	return "%s_%s_ops=%s_feasibility=%s_adoption=%s"%(airport,operation_category_short,ops_scenario,feasibility_scenario,adoption_scenario)

def sidebar():
	import streamlit as st
	st.sidebar.title("WSDOT Electric Aviation 🛩️💡📈")
	# st.sidebar.subheader("Navigation")
	# st.sidebar.info("**Author:** Steffen Coenen")
	st.sidebar.info("**Authors:** Steffen Coenen, Daniel Malarkey, Don MacKenzie")
	st.sidebar.info("**Full material:** The results dataset and all code is available at the corresponding [GitHub repository](https://github.com/s-t-lab/WSDOT-Electric-Aviation).")

"""
#2022-07-11 version
def get_yaxis_range(airport, show_peak, total_2039, hours):
	upper = 1e6
	if airport == "PAE":
		if show_peak:
			if hours >= 6:
				# upper = 43
				upper = 62
			else:
				# upper = 130
				upper = 190
		else:
			# upper = 3700
			upper = 5200
	elif airport == "MWH":
		if show_peak:
			if hours >= 6:
				# upper = 115
				upper = 125
			else:
				# upper = 340
				upper = 375
		else:
			# upper = 9200
			upper = 11000
	
	return (0, upper)
#"""

#current version
def get_yaxis_range(airport, show_peak, total_2039, hours):
	upper = 1e6
	if airport == "PAE":
		if show_peak:
			if hours >= 6:
				# upper = 43
				# upper = 60
				upper = 50.5
			else:
				# upper = 130
				# upper = 180
				upper = 175.5
		else:
			# upper = 3700
			upper = 5000
	elif airport == "MWH":
		if show_peak:
			if hours >= 6:
				# upper = 115
				# upper = 60
				upper = 50.5
			else:
				# upper = 340
				# upper = 240
				upper = 175.5
		else:
			# upper = 9200
			upper = 11000
	
	return (0, upper)
