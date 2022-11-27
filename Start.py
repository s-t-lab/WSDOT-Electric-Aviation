import streamlit as st
import pandas as pd

import utils as u

st.set_page_config(
	page_title="WSDOT Electric Aviation",
	page_icon="🛩️",
	layout="wide",
	initial_sidebar_state="expanded",
)

# import pages
# import app

# """
@st.cache(allow_output_mutation=True)
def get_data():
	data = {}
	# data = []
	
	#operations data
	# df = pd.read_csv("data/ATADS Airport Operations Report (SEA, PAE, MWH)_fix_cleaned.csv", header=7)
	df = pd.read_excel("data/operations/WEB-Report-90921.xlsx", header=7, skipfooter=5)
	df_key = pd.read_csv("data/operations/key.csv", index_col="column_name")
	df.columns = df_key.index
	
	df.columns = [u.snake_case(col) for col in df.columns]
	df = df[~(df["date"].str.contains("Sub-Total").fillna(False))] #remove daily sub-totals from the records
	df["date"] = pd.to_datetime(df["date"])#.dt.date
	df = df.sort_values("facility")
	df = df.set_index(["date", "facility"])
	
	# return df#, df_key
	# return df, df_key
	data["operations"] = [df, df_key]
	# data += [df, df_key]
	
	# st.write(data.keys())
	
	#electricity data
	datasheet = pd.read_excel("data/electricity/Electricity demand projections.xlsx", header=4, sheet_name=None)
	datasheet_key = pd.read_excel("data/electricity/key.xlsx", sheet_name=None)
	data["electricity"] = [datasheet, datasheet_key]
	# data += [datasheet, datasheet_key]
	
	# return df#, df_key
	# return df, df_key
	
	# st.write(data.keys())
	
	return data#, data_key
#"""

data = get_data()
# st.write("here",data.keys())

	

# PAGES = {
	# "Operationsss": pages.operations, 
	# "Electricity demandd": electricity, 
# }

#####

def main():
	# data,data_key = get_data()
	
	u.sidebar()
	
	
	# application architecture
	# selection = st.sidebar.radio("Go to", list(PAGES.keys()))
	# selected_page = st.sidebar.selectbox("Select a page", PAGES.keys())
	# page_names_to_funcs[selected_page]()

	# page = PAGES[selection]

	# with st.spinner(f"Loading {selection} ..."):
		# page.write(data, data_key)

	
	st.header("Electric Aviation at Paine Field and Grant County International Airport 🛩️💡📈")
	# st.write(type(data))
	# st.write("here3",data.keys())
	
	# st.write(dataa)
	
	# st.write(data1)
	# st.write(data2)
	
	st.write("**Link to paper (as accepted by the Transportation Research Board for presentation at the 2023 TRB Annual Meeting):**  \n [Coenen, S., Malarkey, D., MacKenzie, D. (2023). Estimating Electrical Energy and Capacity Demand for Regional Electric Flight Operations at Two Mid-Size Airports in Washington](https://sites.uw.edu/stlab/files/2022/11/Coenen-Malarkey-MacKenzie-TRBAM-23-02419-Electric-Aviation.pdf)")
	
	st.write("**Full material:**  \n The results dataset and all code is available \n at the corresponding [GitHub repository](https://github.com/s-t-lab/WSDOT-Electric-Aviation).")
	
	st.write("**Airports under consideration:**")
	
	col1, col2 = st.columns(2)
	with col1:
		st.write("Grant County International Airport (MWH) \n https://www.portofmoseslake.com/aeronautics/")
		st.image("img/MWH.png")
	with col2:
		st.write("Paine Field/Snohomish County Airport (PAE) \n https://www.painefield.com/")
		st.image("img/PAE.png")

if __name__ == "__main__":
	main()




