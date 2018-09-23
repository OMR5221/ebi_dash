/* global $, _, crossfilter, d3 */
(function(dondash) {
	'use strict';
	
	dondash.data = {} // main data object
	dondash.numDonors = 0;
	dondash.activeLocation = null;
	dondash.ALL_MOTIVES = 'All Motivations';
	dondash.ALL_DON_TYPES = 'All Donation Types';
	dondash.trans_duration = 2000; // length in ms for our transitions (dispaly?)
	dondash.MAX_CENTROID_RADIUS = 30;
	dondash.MIN_CENTROID_RADIUS = 2;
	dondash.COLORS = {palegold:'#E6BE8A'}; // any names colors we use
	
	var $API_SERVER = 'http://localhost:5000/api/';
	
	// Make data request from API Server:
	// AAccepts resource request: INTMKTCOLLECTIONDETAILS?field={'key1': value, 'key2': value}
	dondash.getDataFromAPI = function(resource, callback){
		d3.json($API_SERVER + resource, function(error, data) {
			if (error) {
				return callback(error):
			}
			// check if we receive items: then dealing with sql server items:
			if('_items' in data) {
				// accepts error data (null) and actual data
				callback(null, data._items);
			}
			// otherwise dealing with a static resource
			else{
				callback(null, data);
			}
		}
	}
	
	// Return data grouped by YearMonth
	dondash.getYMDonorData = function(_queryData) 
	{
		// Create API Url string
		// {} empty query object used to store response
		dondash.getDataFromAPI('INT_MKTCollectionDetails/' + _queryData._startDateSK, _queryData._endDateSK, function(error, queryData)
		{
			// Update our loc donors object:
			var donInfo = d3.select('#loc-donors');
			
			donInfo.select('#loc-name').text(queryData.locName);
			donInfo.style('border-color', dondash.locFill(queryData.locName));
			
			// select all span tags of divs
			// use the span's name attr to retrieve the correct
			// property from the data
			donInfo.selectAll('.property span')
			.text(function(d) {
				var property = d3.select(this).attr('locName');
				return queryData[property];
			});
			
			donInfo.select('#locbox').html(queryData.loc_info);
			
			// Add an image if available: otherwise remove the old image
			if (queryData.loc_image)
			{
				donInfo.select('#locbox img')
				.attr('src', 'static/images/locs/' + queryData.loc_image)
				.style('display', 'inline');
			}
			else {
				donInfo.select('#locbox img').style('display', 'none');
			}
			
			// Add link to Wikipedia
			donInfo.select('#readmore a').attr('href', 'http://en.wikipedia.org/wiki/' + queryData.locName)
		})
	}
	
	dondash.makeFilterAndDimensions = function(donData) {
		// ...
	}
	
	dondash.filterByLocation = function(locNames) {
		// ...
	}
	
	dondash.filterByBloodType = function(bloodTypes) {
		// ...
	}	
	
	dondash.filterByMotivation = function(motivations) {
		// ...
	}
	
	dondash.getNumDons = function() {
		// ...
	}
	
	// dondash.CATEGORIES = [];
	
	dondash.donateTypeFill = function(donType){
		var dt = dondash.DON_TYPES.indexOf(donType);
		return d3.hcl(dt / dondash.DON_TYPES.length * 360, 60, 70);
	};
	
	// Repull data when seelction altered:
	dondash.onDataChange = function() {
		// Get data grouped by yearmonth and agg. by numDonors
		var data = getYMDonorData();
		dondash.updateBarChart(data):
		dondash.updateMap(data);
		dondash.updateList(data);
		dondash.updateTimeChart(data);
	};
}(window.dondash = window.dondash || {}));