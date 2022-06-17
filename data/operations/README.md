# Instructions on how to update this app with more recent data

## FAA's Operations Network (OPSNET) data

(daily data (past), which can be aggregated also by month and year)

1. Go to the [FAA's Operations Network (OPSNET)](https://aspm.faa.gov/opsnet/sys/Airport.asp), which reports counts of airport operations as recorded by the Air Traffic Activity System (ATADS).
2. Generate a report selecting the following:
	* *Output:* Standard Report, Show Itinerant + Local, MS Excel Format
	* *Dates:* Go to "Range" tab, select e.g. Jan 1, 2010, until today's date
	* *Facilities:* Enter facility codes of desired airports, e.g. PAE (for Paine Field/Snohomish County Airport), MWH (for Grant County (Moses Lake) Airport), or SEA (for Seattle-Tacoma International Airport)
	* *Filters:* Select none
	* *Groupings:* Select fields "Date" and "Airport"
3. Generate and download report (`.xls`) by clicking *Run*.
4. Open the downloaded file (looks like `WEB-Report-68629.xls`) in Excel and change the date column's format into YYYY-MM-DD, then save the file as a `.xlsx` in this repository's `data` folder.

## FAA's Terminal Area Forecast (TAF) data

(yearly data (past) and forecasts (future))

1. Go to [FAA's Terminal Area Forecast (TAF)](https://taf.faa.gov/), which represents official FAA forecasts of aviation activity (see also [here](https://www.faa.gov/data_research/aviation/taf)).
2. Generate a report selecting the following:
	* Select "Facility", "Detail Report", From 1990, To 2045.
	* In the search field on the right, search for the desired airports (e.g. PAE, MWH, SEA) on after another and confirm it by clicking on the corresponding search result. This way, several airports can be included in the same report output.
	* Ensure that "Create File" is ticked.
3. Generate and download report (`TAFDetailed.txt`) by clicking "Run Report". Store the downloaded file in this repository's `data` folder.
