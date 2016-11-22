# Final Project Proposal
*High level summary of your project, including the things that* **you** *find interesting.*

## Data Plan
*Summarize data sources, data formats, and how to obtain or generate the data you will be using*
I will be creating visualization of a healthcare dataset from Data.gov containing average medicare reimbursement rates for the 100 most common DRG codes for every major hospital in the US. The dataset contains an address for each hospital which I will convert to longitude/latitude coordinates using the Google Maps API. I plan to focus on creating visualizations of the 25 hospitals in Massachusetts. Through these visualizations, I would understand the relationship between the geographic locations of hospitals and the rate at which they are reimbursed by medicare for various procedures.

## Implementation Plan
*Overview of you plan. Are you starting from existing code? What skills from the course will be be using to complete your project? etc.*
To create the outline of MA for the map I should be able to reuse code for drawing state maps from Lab 6 (Purple America). I plan to adapt code from labs 5-6 and lecture 29 to draw circles with size and color proportional to the data. 
I will be using methods from the unsupervised section of the Yelp Maps project
(http://nifty.stanford.edu/2016/hou-zhang-denero-yelp-maps/maps/index.html) to geographically cluster hospitals with similar reimbursement rates.

### External Libraries
- Dataset from Center for Medicare & Medicaid Services (CMS) of average medicare reimbursement per hospital for the 100 most common inpatient services  https://data.cms.gov/Medicare/Inpatient-Prospective-Payment-System-IPPS-Provider/97k6-zzx3
- Google Maps Geocoding API
- US map/state map coordinates from Lab 6: Purple America

### Milestones
- Create a new column in the data containing average patient contribution (total reimbursement received by hospital - medicare reimbursement)
- Convert hospital addresses to longitude/latitude coordinates
- Generate map of MA with hospital locations marked
- Generate map of MA with hospital locations marked
- Cluster hospitals based on reimbursement rate for a given procedure

## Deliverables
- Map of MA with hospitals marked by circles where size is proportional to number of dischanrges and color is proportional to average reimbursement (for a specific medical procedure)
- Voronoi Diagram Map of MA hospitals grouped by average reimbursement rate (for a specific medical procedure)

# Final Project Report
*What you have achieved/learned*

*What open questions remain*

## Instructions to run the code
