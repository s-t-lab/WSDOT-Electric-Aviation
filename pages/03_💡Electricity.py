import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import utils as u

from Start import data

save_figure = 0 #set to True if using this tool locally to output the figures

u.sidebar()

datasheet, datasheet_key = data["electricity"]

st.header("Plausible Electricity Demand for Electric Aviation at PAE and MWH 📈💡")


# st.write("this is the electricity.py file")

# st.write(datasheet_key)

# st.write(datasheet["Start"])

output_vars = {"Annual energy [MWh]" : "Electricity demand (energy)", 
				"Average power [kW]" : "Electricity demand (power, aver", 
				"Peak power [MW]" : "Electricity demand (power, peak", 
		}
ylabels = {	"Electricity demand (energy)" : "Annual energy [MWh]", 
			"Electricity demand (power, aver" : "Average power [kW]", 
			"Electricity demand (power, peak" : "Peak power [MW]", 
		}
hovertemplates = {"Electricity demand (energy)" : "%{y:.1f} MWh", 
				"Electricity demand (power, aver" : "%{y:.0f} kW", 
				"Electricity demand (power, peak" : "%{y:.1f} MW", 
		}
colors = {
			"Local Civil" : "#1f77b4", 
			"Itinerant General Aviation" : "#d62728", 
			"Itinerant Air Taxi" : "#2ca02c", 
			"eVTOL" : "#9467bd", 
			"Total" : "#7f7f7f", 
		}

col01, col02 = st.columns(2)
with col01:
	output_var = output_vars[st.selectbox("Output variable (annual energy/average power/peak power):", output_vars.keys(), index=2)]
# st.write(datasheet.keys())
# df = datasheet["Electricity demand (energy)"]#.T
df = datasheet[output_var]#.T

df_key = datasheet_key["dimensions"]
df_key.index = df_key["column_name"]

airports = df_key.loc["airport", "values"].split(",")
operation_categories = df_key.loc["operation_category", "values"].split(",")
ops_scenarios = df_key.loc["ops_scenario", "values"].split(",")
feasibility_scenarios = df_key.loc["feasibility_scenario", "values"].split(",")
adoption_scenarios = df_key.loc["adoption_scenario", "values"].split(",")
operation_categories_short = dict(zip(operation_categories, df_key.loc["operation_category_short", "values"].split(",")))
# st.write(operation_categories_short)

labels = []
for airport in airports:
	for operation_category in operation_categories:
		for ops_scenario in ops_scenarios:
			for feasibility_scenario in feasibility_scenarios:
				for adoption_scenario in adoption_scenarios:
					labels += [u.get_label(airport, operation_categories_short[operation_category], ops_scenario, feasibility_scenario, adoption_scenario)]
# st.write(labels)

# multiindex = pd.MultiIndex.from_product([airports, operation_categories, ops_scenarios, feasibility_scenarios, adoption_scenarios], names=["airport", "operation_category", "ops_scenario", "feasibility_scenario", "adoption_scenario"])
# st.write(multiindex)
# st.write(list(df_key["name_in_xlsx"]))
df = df.drop([name_in_xlsx for name_in_xlsx in list(df_key["name_in_xlsx"]) if "short" not in name_in_xlsx], axis=1)
df = df.T
df.index = df.index.astype(int)
df = df.loc[(df.index >= 2020) & (df.index <= 2040)]

df.columns = labels


# index_col=["airport", "operation_category", "ops_scenario", "feasibility_scenario", "adoption_scenario"]

# df.index = df_key.index

# df.columns = [u.snake_case(col) for col in df.columns]
# df = df[~(df["date"].str.contains("Sub-Total").fillna(False))] #remove daily sub-totals from the records
# df["date"] = pd.to_datetime(df["date"])#.dt.date
# df = df.sort_values("facility")
# df = df.set_index(["date", "facility"])

# st.write(data)
# st.write(type(data))
# st.write(df)
# st.write(df_key.head())


col11, col12 = st.columns(2)
with col11:
	airport = st.selectbox("Airport:", airports)
with col12:
	# operation_categories_selected = st.multiselect("Operation category:", operation_categories, default=[operation_category for operation_category in operation_categories if "Total" not in operation_category if "eVTOL" not in operation_category])
	operation_categories_selected = st.multiselect("Operation category:", operation_categories, default=[operation_category for operation_category in operation_categories if "Total" not in operation_category])
st.write("**Scenarios:**")
col21, col22, col23 = st.columns(3)
with col21:
	ops_scenario = st.selectbox("No. of ops. growth scenario:", ops_scenarios, index=1)
with col22:
	feasibility_scenario = st.selectbox("Feasibility rate scenario:", feasibility_scenarios, index=1)
with col23:
	adoption_scenario = st.selectbox("Adoption rate scenario:", adoption_scenarios, index=1)
if "peak" in output_var:
	col31, col32, col33 = st.columns(3)
	with col31:
		hours = st.selectbox("All charging occurs in how many hours?", range(2,25,2), index=3)

# yaxis_ranges = {"PAE": [0,32000], "MWH": [0,75000]}

# aggregation by day/month/year
# agg_options = ["Day", "Month", "Year"]
# aggregation = st.radio("Aggregate data by:", agg_options, index=agg_options.index("Month"))

# data_source = "OPSNET"
# data_sources = ["OPSNET", "TAF"]
# if aggregation == "Year":
	# data_source = st.radio("Take data from:", data_sources, index=data_sources.index("OPSNET"))

# if data_source == "OPSNET":
	# df_fac = df.loc[(slice(None), fac), :]
	# df_fac.index = df_fac.index.droplevel("facility")
# elif data_source == "TAF":
	# df_TAF = pd.read_csv("data/TAFDetailed.txt", delimiter="\t") #read TAF data
	# first_forecasted_year = df_TAF.loc[df_TAF["SCENARIO"] == 1, "SYSYEAR"].iloc[0]
	# st.write("**Note:** The shown values are forecasts (not actual data) for %d and all following years."%first_forecasted_year)
	
	#process TAF data (drop not needed columns, rename columns)
	# df_TAF = df_TAF.drop(["Region", "APORT_NAME", "CITY", "STATE", "FAC_TYPE", "ATCT_FLAG", "HUB_SIZE", "SCENARIO", "TOT_BA", "AC", "COMMUTER", "T_ENPL", "T_TROPS"], axis=1)
	# df_TAF["date"] = pd.to_datetime(df_TAF["SYSYEAR"], format="%Y")
	# df_TAF = df_TAF.drop("SYSYEAR", axis=1)
	# rename_dict = dict(zip(df_key["name_in_TAF"], df_key.index))
	# df_TAF = df_TAF.rename(rename_dict, axis=1)
	# df_TAF["facility"] = df_TAF["facility"].str.replace(" ", "")
	# df_TAF = df_TAF.set_index(["date", "facility"])
	
	#save data as csv
	# df_TAF.to_csv("data/aggregations/data_TAF.csv")
	
	#select data only for the selected airport (facility)
	# df_fac = df_TAF.loc[(slice(None), fac), :]
	# df_fac.index = df_fac.index.droplevel("facility")

#default (date)range to be selected
# if aggregation == "Day":
	# range = [max(pd.to_datetime("2018-12-31 12:00:00"), df_fac.index.min()-pd.Timedelta(0.5, "d")), df_fac.index.max()]
# elif aggregation == "Month":
	# range = [max(pd.to_datetime("2018-12-05"), df_fac.index.min()-pd.Timedelta(26, "d")), df_fac.index.max()]
# elif aggregation == "Year":
	# range = [max(pd.to_datetime("2018-06-01"), df_fac.index.min()-pd.Timedelta(214, "d")), pd.to_datetime("%s-08-01"%df_fac.index.max().year)]
range = [2019,2041]

# show totals or grouped by category
# options = ["By category", "Total"]
# chart = st.radio("Show total number of operations or by operation category:", options, index=options.index("By category"))

fig = go.Figure()

fsize = 18
if save_figure:
	fsize = 22
# ffactor = 0.75
ffactor = 0.85

# layout options of the graph
layout = dict(
	height=600, 
	xaxis_title = "<b>Year</b>", 
	yaxis_title = "<b>%s</b>"%ylabels[output_var], 
	xaxis_title_font_color = "black", 
	yaxis_title_font_color = "black", 
	xaxis_title_font_size = fsize, 
	yaxis_title_font_size = fsize, 
	xaxis_tickfont_color = "black", 
	yaxis_tickfont_color = "black", 
	yaxis_gridcolor = "grey", 
	# xaxis_tickfont_size = fsize, 
	xaxis_tickfont_size = fsize*ffactor, 
	yaxis_tickfont_size = fsize*ffactor, 
	hoverlabel_namelength=-1, #do not truncate the hoverlabels
	
	# yaxis_range = yaxis_ranges[airport], 
	xaxis = dict(
		rangeslider = dict(
			visible = True, 
		),
		# type = "date", 
		range = range, 
	), 
	barmode="stack", 
	showlegend=True, 
	hovermode='x unified', 
	legend=dict(
		yanchor="bottom",
		y=1.02,
		xanchor="center",
		x=0.5
	),
	legend_orientation="h"
)
fig.update_layout(layout)
# fig.update_xaxes(ticklabelmode="period")

# if aggregation == "Day":
	# dff = df_fac
# elif aggregation == "Month":
	# df_fac_byM = df_fac.resample("M").sum()
	# df_fac_byM.index = [pd.to_datetime("%d-%d-01"%(datetime.year, datetime.month)) for datetime in df_fac_byM.index]
	# dff = df_fac_byM
	# fig.update_layout(xaxis=dict(dtick="M1"))
# elif aggregation == "Year":
	# df_fac_byY = df_fac.resample("Y").sum()
	# df_fac_byY.index = [pd.to_datetime("%d-01-01"%(datetime.year)) for datetime in df_fac_byY.index]
	# dff = df_fac_byY
	# fig.update_layout(xaxis=dict(tickformat = "%Y", dtick="M12"))

# dff.to_csv("data/aggregations/data_%s_by%s_from%s.csv"%(fac,aggregation,data_source))

# if chart == "By category":
	# for cat in categories.keys():
	# for cat in categories:
		# fig.add_trace(go.Bar(x=dff.index, y=dff[cat], name=categories[cat]))
		# fig.add_trace(go.Bar(x=dff.index, y=dff[cat], name=df_key.loc[cat, "name"]))
# elif chart == "Total":
	# fig.add_trace(go.Bar(x=dff.index, y=dff["total"], name="Total no. of operations"))
for operation_category in operation_categories_selected:
	label = u.get_label(airport, operation_categories_short[operation_category], ops_scenario, feasibility_scenario, adoption_scenario)
	# st.write(label)
	y = df[label]
	if "peak" in output_var:
		y /= 1000 #kW to MW
	if "peak" in output_var:
		y *= 8/hours
	# st.write(operation_category)
	fig.add_trace(go.Bar(x=df.index, y=y, name=operation_category, marker_color=colors[operation_category], 
							hovertemplate = hovertemplates[output_var]
	))
	# st.write(y)

if "power" in output_var:
	total_label = u.get_label(airport, "Total", ops_scenario, feasibility_scenario, adoption_scenario)
	show_peak = True if "peak" in output_var else False
	if not show_peak:
		hours = None #because it wasn't defined before (and is not needed in this case)
	fig.update_layout(dict(yaxis_range = u.get_yaxis_range(airport, show_peak, df.loc[2039, total_label], hours)))

if "aver" in output_var:
	fig.add_hline(y=2500, line_color="orange")
	fig.add_hline(y=10000, line_color="purple")
if "peak" in output_var:
	fig.add_hline(y=2.5, line_color="orange")
	fig.add_hline(y=10, line_color="purple")
# fig.update_layout(dict(yaxis_range = None)) # in case no custom yaxis ranges are desired
# fig.update_layout(font=dict(size=18))

if "power" in output_var:
	y = df[total_label]
	if "peak" in output_var:
		y *= 8/hours
	try:
		year2_5 = str(y[y > 2500].index.tolist()[0])
	except:
		year2_5 = "/"
	try:
		year10 = str(y[y > 10000].index.tolist()[0])
	except:
		year10 = "/"
	st.markdown('- First year with total power above 2.5 MW: <font color="orange">**%s**</font>\n- First year with total power above 10 MW: <font color="purple">**%s**</font>'%(year2_5,year10), unsafe_allow_html=True)

fig.update_layout(yaxis=dict(tickformat = ","))

if save_figure:
	# fig.update_layout(yaxis_title_standoff=15, yaxis_automargin=True)
	fig.update_layout(yaxis_title_standoff=10, yaxis_automargin=True)
	
	# width = 1000
	# width = fsize*1000/22
	width = fsize*750/22
	fig.write_image("img/plots/ele/ele_{0:s}_{1:s}_{2:3s}_{3:3s}_{4:3s}.png".format(airport,output_var,ops_scenario, feasibility_scenario, adoption_scenario), width=width, height=0.8*width, scale=5)

st.plotly_chart(fig, sharing="streamlit", use_container_width=True)
