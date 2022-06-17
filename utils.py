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
	st.sidebar.info("**Full material:** The results dataset and all code is available at the corresponding [GitHub repository](https://github.com/steffen-coe/...).")
