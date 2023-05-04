import streamlit as st
import pandas as pd
import plotly.graph_objects as go

import utils as u

from Start import data

save_figure = 0 #set to True if using this tool locally to output the figures

u.sidebar() #this likely needs to be after the "from Start import data" line, because otherwise the st.set_page_config() command is run more than once, which leads to an error

df, df_key = data["operations"]

colors = {
			"lcl_civil" : "#1f77b4", 
			"itin_ga" : "#d62728", 
			"itin_taxi" : "#2ca02c", 
			"itin_carrier" : "#ff7f0e", 
			"itin_military" : "#8c564b", 
			"lcl_military" : "#e377c2", 
			"Total" : "#7f7f7f", 
		}

# st.write(df_key)


#save data as csv
# df.to_csv("data/operations/aggregations/data_OPSNET.csv")

# categories = {"itin_carrier" : "Itinerant Air Carrier", "itin_taxi" : "Itinerant Air Taxi", "itin_ga" : "Itinerant General Aviation", "itin_military" : "Itinerant Military", "lcl_civil" : "Local Civil", "lcl_miltary" : "Local Military"}
categories = [col for col in df.columns if "total" not in col]

st.header("Operations at PAE and MWH Airports 🛩️")

st.write("Explore the number of operations (take-offs and landings) at each of the following three airports.")
st.write("+ Grant County International Airport (MWH), at Moses Lake\n + Paine Field/Snohomish County Airport (PAE)\n + Seattle-Tacoma International Airport (SEA)")

fac = st.selectbox("Airport:", df.index.levels[1].to_list())

st.write("Data can be taken from one of the following sources:\n + [FAA's Operations Network (OPSNET)](https://aspm.faa.gov/opsnet/sys/Airport.asp), reporting counts of airport operations as recorded by the Air Traffic Activity System (ATADS)\n   * Can be aggregated by day, month, or year\n + [FAA's Terminal Area Forecast (TAF)](https://taf.faa.gov/), representing official FAA forecasts of aviation activity (see also [here](https://www.faa.gov/data_research/aviation/taf))\n   * Only available by year")
	
# aggregation by day/month/year
agg_options = ["Day", "Month", "Year"]
aggregation = st.radio("Aggregate data by:", agg_options, index=agg_options.index("Month"))

data_source = "OPSNET"
data_sources = ["OPSNET", "TAF"]
if aggregation == "Year":
	data_source = st.radio("Take data from:", data_sources, index=data_sources.index("OPSNET"))

if data_source == "OPSNET":
	df_fac = df.loc[(slice(None), fac), :]
	df_fac.index = df_fac.index.droplevel("facility")
elif data_source == "TAF":
	df_TAF = pd.read_csv("data/operations/TAFDetailed.txt", delimiter="\t") #read TAF data
	first_forecasted_year = df_TAF.loc[df_TAF["SCENARIO"] == 1, "SYSYEAR"].iloc[0]
	st.write("**Note:** The shown values are forecasts (not actual data) for %d and all following years."%first_forecasted_year)
	
	#process TAF data (drop not needed columns, rename columns)
	df_TAF = df_TAF.drop(["Region", "APORT_NAME", "CITY", "STATE", "FAC_TYPE", "ATCT_FLAG", "HUB_SIZE", "SCENARIO", "TOT_BA", "AC", "COMMUTER", "T_ENPL", "T_TROPS"], axis=1)
	df_TAF["date"] = pd.to_datetime(df_TAF["SYSYEAR"], format="%Y")
	df_TAF = df_TAF.drop("SYSYEAR", axis=1)
	rename_dict = dict(zip(df_key["name_in_TAF"], df_key.index))
	df_TAF = df_TAF.rename(rename_dict, axis=1)
	df_TAF["facility"] = df_TAF["facility"].str.replace(" ", "")
	df_TAF = df_TAF.set_index(["date", "facility"])
	
	#save data as csv
	# df_TAF.to_csv("data/operations/aggregations/data_TAF.csv")
	
	#select data only for the selected airport (facility)
	df_fac = df_TAF.loc[(slice(None), fac), :]
	df_fac.index = df_fac.index.droplevel("facility")

#default (date)range to be selected
if aggregation == "Day":
	range = [max(pd.to_datetime("2018-12-31 12:00:00"), df_fac.index.min()-pd.Timedelta(0.5, "d")), df_fac.index.max()]
elif aggregation == "Month":
	range = [max(pd.to_datetime("2018-12-05"), df_fac.index.min()-pd.Timedelta(26, "d")), df_fac.index.max()]
elif aggregation == "Year":
	range = [max(pd.to_datetime("2014-06-01"), df_fac.index.min()-pd.Timedelta(214, "d")), pd.to_datetime("%s-08-01"%df_fac.index.max().year)]

# show totals or grouped by category
options = ["By category", "Total"]
chart = st.radio("Show total number of operations or by operation category:", options, index=options.index("By category"))

fig = go.Figure()

fsize = 18
if save_figure:
	fsize = 22
ffactor = 0.75

# layout options of the graph
layout = dict(
	height=600, 
	xaxis_title = "<b>Date</b>", 
	yaxis_title = "<b>Number of operations</b>", 
	xaxis_title_font_color = "black", 
	yaxis_title_font_color = "black", 
	xaxis_title_font_size = fsize, 
	yaxis_title_font_size = fsize, 
	xaxis_tickfont_color = "black", 
	yaxis_tickfont_color = "black", 
	yaxis_gridcolor = "grey", 
	xaxis_tickfont_size = fsize, 
	yaxis_tickfont_size = fsize*ffactor, 
	hoverlabel_namelength=-1, #do not truncate the hoverlabels
	xaxis = dict(
		rangeselector = dict(
			buttons=list([
				dict(count=1,
					 label="1m",
					 step="month",
					 stepmode="backward"),
				dict(count=6,
					 label="6m",
					 step="month",
					 stepmode="backward"),
				dict(count=1, 
					 label="1y", 
					 step="year", 
					 stepmode="backward"),
				dict(count=1, 
					 label="YTD", 
					 step="year", 
					 stepmode="todate"),
				dict(step="all")
			])
		),
		rangeslider = dict(
			visible = True, 
		),
		type = "date", 
		range = range, 
	), 
	barmode="stack", 
	showlegend=True, 
	hovermode='x unified', 
)
fig.update_layout(layout)
# fig.update_xaxes(ticklabelmode="period")

if aggregation == "Day":
	dff = df_fac
elif aggregation == "Month":
	df_fac_byM = df_fac.resample("M").sum()
	df_fac_byM.index = [pd.to_datetime("%d-%d-01"%(datetime.year, datetime.month)) for datetime in df_fac_byM.index]
	dff = df_fac_byM
	fig.update_layout(xaxis=dict(dtick="M1"))
elif aggregation == "Year":
	df_fac_byY = df_fac.resample("Y").sum()
	df_fac_byY.index = [pd.to_datetime("%d-01-01"%(datetime.year)) for datetime in df_fac_byY.index]
	dff = df_fac_byY
	fig.update_layout(xaxis=dict(tickformat = "%Y", dtick="M12"))

# dff.to_csv("data/operations/aggregations/data_%s_by%s_from%s.csv"%(fac,aggregation,data_source))

if chart == "By category":
	# for cat in categories.keys():
	for cat in categories:
		# fig.add_trace(go.Bar(x=dff.index, y=dff[cat], name=categories[cat]))
		# st.write(cat)
		fig.add_trace(go.Bar(x=dff.index, y=dff[cat], name=df_key.loc[cat, "name"], marker_color=colors[cat]))
elif chart == "Total":
	fig.add_trace(go.Bar(x=dff.index, y=dff["total"], name="Total no. of operations", marker_color=colors["Total"]))
fig.update_layout(yaxis=dict(tickformat = ","))

if save_figure:
	range_for_export = [pd.to_datetime("2014-06-01"), pd.to_datetime("2021-08-01")]
	fig.update_layout(xaxis_range=range_for_export) #range

	fig.update_layout(yaxis_title_standoff=15, yaxis_automargin=True)
	fig.update_layout(yaxis_dtick = 20000)
	
	# width = 1000
	width = fsize*1000/22
	fig.write_image("img/plots/ops/ops_%s.png"%fac, width=width, height=0.65*width, scale=5)

st.plotly_chart(fig, sharing="streamlit", use_container_width=True)


