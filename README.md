# Final Project Proposal
*High level summary of your project, including the things that* **you** *find interesting.*

The programs I created, generate map visualizations of data related to reimbursements received by hospitals. I combined skills from previous labs for creating map visualizations and using class objects to organize information. Trying to visualize this information for geospacial analysis required making decisions about how to scale/represent different values associated with each hospital. Potential expansions of this project include experimenting with different methods of representing the range of values using color (eg. color proportional to the value's distance from the mean or the median)

## Data Plan
*Summarize data sources, data formats, and how to obtain or generate the data you will be using*

I will be creating visualization of a healthcare dataset from Data.gov containing average medicare reimbursement rates for the 100 most common DRG codes for every major hospital in the US. The dataset contains an address for each hospital which I will convert to longitude/latitude coordinates using the Google Maps API. I plan to focus on creating visualizations of the 25 hospitals in Massachusetts. Through these visualizations, I would understand the relationship between the geographic locations of hospitals and the rate at which they are reimbursed by medicare for various procedures.

## Implementation Plan
*Overview of you plan. Are you starting from existing code? What skills from the course will be be using to complete your project? etc.*

To create the outline of MA for the map I should be able to reuse code for drawing state maps from Lab 6 (Purple America). I plan to adapt code from labs 5-6 and lecture 29 to draw circles with size and color proportional to the data (Stock Viz).

### External Libraries
- Dataset from Center for Medicare & Medicaid Services (CMS) of average medicare reimbursement per hospital for the 100 most common inpatient services  https://data.cms.gov/Medicare/Inpatient-Prospective-Payment-System-IPPS-Provider/97k6-zzx3
- Google Maps Geocoding API
- US map/state map coordinates from Lab 6: Purple America

### Milestones
- Create a new column in the data containing average patient contribution (total reimbursement received by hospital - medicare reimbursement)
- Convert hospital addresses to longitude/latitude coordinates
- Generate map of MA with hospital locations marked
- Generate map of MA with hospital locations marked by circles proportional to number of discharges

## Deliverables
- Map of MA with hospitals marked by circles where size is proportional to number of discharges and color is proportional to reimbursement (for a specific medical procedure)

# Final Project Report

*What you have achieved/learned*

In writing code to create the underlying geographic maps I discovered that with the coordinates given I couldn't use the polygon function to just create outlines (unfilled) of states/region.

I created some interesting and aesthetically appealing visualizations of this information. I realized that without a standard scale for color and circle size, I couldn't compare visualizations of different states to analyze trends. I chose to resolve this issue by writing code to create maps of multiple states/regions. Another solution might have been to write code to determine an appropriate scale to apply to all maps of the same metric or code to draw a legend in the corner of the visualizations.

I also tried to write code for visualizing the entire US but I am not completely confident my visualization is accurate. Because of the way I set up my program, every time I run the program it geocodes all of the hospitals. Even for rare DRG codes, this causes each run to take a substantial amount of time (20-30min)and made debugging the process difficult. I found out that 2,500 API queries is not that much. On multiple occasions in debugging/running my code I exhausted the quota for queries associated with my API key!

*What open questions remain*

-What's the best way to color code the circles by the magnitude of reimbursement?

For simplicity I colored them on a linear scale so that the maximum value is bright green, the minimum value is bright red and the value exactly between the two will be white. It might make more sense to set the average as white and have color proportional to distance from the mean. It could also be useful to specify a discrete set of possible colors and group values by number of standard deviations from the mean.

-Is it possible to create a more efficient method for geocoding hospitals?

Every time the make_map.py program is run it collect hospital info/addresses and geocodes it. The geocoding process is the most time intensive part of the process. Running the program to make multiple maps of the same hospitals lead to a lot of repeat geocoding. It might be more efficient to geocode all hospitals once and make a dictionary of their coordinates or write the geocoded coordinates into the csv.

## Instructions to run the code

make_map.py is set up to make maps of a single state, multiple states or the entire US.

There are several possible variables for the map to visualize (possible parameters):
  C = "Charge", the average charge billed by the hospital for the given DRG code
  T = "Total", the average total reimbursement/payment the hospital received for the given DRG code
  M = "Medicare", the average total reimbursement from medicare for the given DRG
  P = "Paydiff", the difference between "Charge" and "Total"

General format:

$ python3 make_map.py <Number of states> <State abbrev. 1> ... <State abbrev. n> <DRG code> <parameter>

Example: To make a plot of total reimbursement in MA hospitals for DRG code 470 (file will be automatically saved as "MA_039_T.png")

$ python3 make_map.py MA 470 T

Example: To make a plot of US medicare reimbursement for DRG code 039 (file will be automatically saved as "US_039_M.png")

$ python3 make_map.py 1 US 039 M

Note: if the map comes up blank (no circles) it means the quota for queries with this API key has been reached
