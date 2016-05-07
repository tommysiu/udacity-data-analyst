## Making Effective Data Visualization Project
By Tommy Siu - 7 May 2016

### Summary
The dataset contains 113,937 loan data records from Prosper.
In this project I mainly focus on the relationship between original loan amount, the state of address of the borrowers, and the year which the loans were originated. I would like to know the loan amount of each state over the years.

The final visualization shows that state California continued to be the top loan amount state from year 2006 to 2014. It can also be seen that the overall loan amount was decreased sharply in 2009, which was due to global financial crisis at that time.

### Design
The data file prosperLoanData.csv contains 113,937 records with 81 variables. I noticed that there is a variable named BorrowerState which records the originated state of the loan. I wondered if there is any relationship between the overall loan amount and the location within United States. Thus I decided to show the loan amount per each location.

	data[['BorrowerState', 'LoanOriginalAmount']].groupby(['BorrowerState'], as_index=False).sum()

By grouping the BorrowerState and summing up the LoanOriginalAmount variable, I can see which states made the most significant loan contributions. However, very soon I was aware that this information was not sufficient for a meaningful visualization because it did not include the time element, which is usually important in data visualization. Thus I created a new **year** variable to capture the year of LoadOriginationDate variable and group the loan amount by both state and year.

	data['year'] = data['LoanOriginationDate'].apply(lambda x: x[:4])
	df = data[['BorrowerState', 'year', 'LoanOriginalAmount']].groupby(['BorrowerState','year']).sum()

To make the visualization more interesting, I decided to adopt the [d3.geomap](https://d3-geomap.github.io/) library so user can get a bit more information about the geographic location of the state.

I used a horizontal bar chart to indicate the loan amount of each state. I think it should be the appropriate chart type as the state variable is categorical data and bar chart provides a good visual representation of that. 

### Visualization
The original visualization is shown below. It is composed of a list of buttons to select the year, a geo map to show the state locations, and a bar chart for the top 10 states for largest loan amount. I used the geomap built-in Reds color scheme to indicate the loan amount of each state. In the bar chart, I fixed the x-scale so that reader can notice the changes when he switches the year. 

![Initial Chart](https://raw.githubusercontent.com/tommysiu/udacity-data-analyst/master/P5-data-visualization-and-D3/screen_initial.png)


### Feedback
After I created the visualization I shared it with several friends and asked for their comments. 

#### Comment #1
The first comment is about the missing bar chart title. As I think it may not be a good idea to list all states, I limited the chart to show the top 10 states only. I sorted the states by the total loan amount throughout the year and thought the meaning was obvious. However, I think a proper chart title is very important to let the readers know what exactly it is about. I also added back the x-axis title to indicate it is about the loan amount.

#### Comment #2
The second comment is about the lack of interaction between the bar chart and the map. While the bar chart showed the top 10 states, there was no linkage between it and the map. Thus I added an interaction to the bar chart, which would highlight the state in the map when the bar item is clicked.

#### Comment #3
The last comment is about the default behaviour of d3.geomap. When a reader clicks a particular state, the map would be translated to centre the state. While I set the zoom level to 1 (i.e. no zooming), the map still moves when the state is being clicked. Finally I checked a bit of the d3.geomap source code and override the map clicked function in order to disable zooming completely. 

#### Comment #4
My friend also pointed out that when the year was selected, the bar changes should be animated in order to have a more impressive visualization. Therefore I modified the d3 selection of the bar items such that the width of the data items will be transited to their latest width in 0.5 second.

### Final Visualization
I updated the visualization based on the comments and the final result is shown below.

![Final Chart](https://raw.githubusercontent.com/tommysiu/udacity-data-analyst/master/P5-data-visualization-and-D3/screen_final.png)


### Resources
- D3.geomap library - [https://d3-geomap.github.io/](https://d3-geomap.github.io/)
- USA state hash table - [https://gist.github.com/mshafrir/2646763](https://gist.github.com/mshafrir/2646763)
- D3 Tick Format - [https://bl.ocks.org/mbostock/9764126](https://bl.ocks.org/mbostock/9764126)
- D3 Transition - [https://github.com/mbostock/d3/wiki/Transitions](https://github.com/mbostock/d3/wiki/Transitions)



