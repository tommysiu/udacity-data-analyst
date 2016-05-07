d3 = Promise.promisifyAll(d3);

var bar_width = window.screen.width * 0.5 - 100;
var x_bar_offset = 90;
var x_tick_value = 5000000;
var loan_data;
var state_name = {};
var state_abbr = {};
var state_fips = {};
var years = [];
var max_year = 0;
var x_scale, y_scale;
var y_axis;

// the geomap configuration
var map = d3.geomap.choropleth()
  .geofile('data/USA.json')
  .height(window.screen.height * 0.6)
  .projection(d3.geo.albersUsa)
  .unitId('fips')
  .format(d3.format('$,.0f'))
  .colors(colorbrewer['Reds'][9])
  .scale(700)
  .zoomFactor(1)
  .legend(true);

// add a bar chart
var svg = d3.select('#bar')
  .append('svg')
  .attr('width', bar_width)
  .attr('height', 600)
  .append('g')
  .attr('class', 'chart');

// function to update the charts with particular year data
var update_data = function(year) {
  d3.selectAll('.years_buttons')
    .selectAll('div')
    .transition()
    .duration(200)
    .style('color', 'black')
    .style('background', '#fbc97f');

  d3.selectAll('.years_buttons div')
    .filter(function(d) {
      return d == year; 
    })
    .transition()
    .duration(300)
    .style('color', 'black')
    .style('background', 'lightBlue');

  var sorted_data = loan_data.sort(function(a,b){
    return b[year] - a[year];
  });

  // redraw y axis and update labels for the year
  var y_labels = [];
  for(i in sorted_data) {
    y_labels.push(state_name[sorted_data[i]['BorrowerState']]);
  }
  y_axis.tickFormat(function(d,i){ 
    return y_labels[i]; 
  });
  svg.select('#yaxis').call(y_axis);

  // select the bar items and bind the data
  var bars = svg.select('g.bars')
    .selectAll('rect')
    .data(sorted_data.slice(0,10),function(d){
      return d[year];
    });

  // update existing items
  bars.attr('x',0)
    .attr('y', function(d,i){
      return y_scale(i) + 10;
    })
    .attr('width', function(d) {
      return x_scale(d[year]);
    })

  // update new items
  bars.enter()
    .append('rect')
    .attr('id',(function(d){
      return state_fips[d['BorrowerState']];
    }))
    .attr('height',22)
    .attr('x',0)
    .attr('y', function(d,i){
      return y_scale(i) + 10;
    })
    .attr('width', function(d) {
      if(isNaN(d[year]))
        return 0;
      return x_scale(d[year]);
    });

  // remove exit items
  bars.exit()
    .attr("width", 0)
    .remove();

  // update map with correct year
  map.column(year);
  map.update();

};

// load the state hash and name conversion table
d3.jsonAsync('data/states_hash.json').then(function(dict){
  state_name = dict;
  state_abbr = _.invert(dict);

  // loaded the loan data
  return d3.csvAsync('data/loan_amounts_by_year.csv');

}).then(function(data){
  loan_data = data;

  // find max year
  for(k in data[0]) {
    if(k !== 'BorrowerState') {
      years.push(k);
      if(k > max_year) {
        max_year = k;
      }
    }
  }

  // find overall max loan to fix the x-axis scale
  var max_loan = d3.max(data, function(d){
    var values = [];

    // find a state's max loan value spanning all years
    for(key in d) {
      if(key != 'BorrowerState')
        values.push(parseFloat(d[key]));
    }
    return d3.max(values);
  });

  // create buttons for available years
  var buttons = d3.select('.years_buttons')
    .selectAll('div')
    .data(years)
    .enter()
    .append('div')
    .attr('id', function(d) {
      return d;
    })
    .attr('class', 'year')
    .text(function(d){
      return d;
    });

  // call update_data when button is clicked
  buttons.on("click", update_data);

  // determine x and y scales
  x_scale = d3.scale.linear()
    .domain([0, max_loan*1.3])
    .range([0,bar_width]);

  y_scale = d3.scale.linear()
    .domain([-1, 9.5])
    .range([0,350]);

  // draw x axis
  svg.append('g')
    .attr('transform', 'translate(' + x_bar_offset + ',30)')
    .attr('id','xaxis');
  x_axis = d3.svg.axis();
  x_axis.orient('bottom')
    .ticks(10)
    .scale(x_scale)
    .tickValues(d3.range(0, max_loan + x_tick_value, x_tick_value))
    .tickFormat(d3.format("s"));

  // add x-axis and title
  svg.select('#xaxis').call(x_axis);

  // draw y axis
  svg.append('g')
    .attr('transform', 'translate(' + (x_bar_offset-10) + ',30)')
    .attr('id','yaxis');
  y_axis = d3.svg.axis();
  y_axis.orient('left')
    .scale(y_scale)
    .tickValues(d3.range(10));

  svg.append('g')
    .attr('class', 'bars')
    .attr("transform", "translate(" + x_bar_offset + ",10)");

  return d3.jsonAsync('data/USA.json');

}).then(function(map_data){

  // get the fips code for all states from the map data
  var paths = map_data.objects.units.geometries;
  for(i in paths) {
    state_fips[state_abbr[paths[i].properties.name]] = paths[i].id;
  }

  // update the data item with fips code
  for(i in loan_data) {
    loan_data[i].fips = state_fips[loan_data[i].BorrowerState];
  }
  d3.select('#map').datum(loan_data).call(map.draw, map);

  // draw the bar char
  update_data(max_year);
});
