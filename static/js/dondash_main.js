(function(dondash) {
	'use strict';
	
	var query_collectDetails = 'INT_MKTCollectionDetails?' + JSON.stringify( {"year_month":0, "don_type": 0, "loc_name": 0, "num_donors":0} )

	// Look into queueing with Redis:
	var queue = queue()
		.defer(d3.json, "static/data/us-10m.json")
		// Make call to the api:
		.defer(dondash.getDataFromAPI, query_collectDetails)

	// The $STATIC_API flag dictates whether we are using static
    // files or using the MongoDB based EVE-API
    if(window.$STATIC_API)
	{
        q.defer(dondash.getDataFromAPI, '_donorData');
    }
    else{
		// Make call to the api:
		.defer(dondash.getDataFromAPI, query_collectDetails)
    }
    
    q.await(ready);
		
	function ready(error, usMap, locNames, donType, ymCollectDtlData)
	{
		// Log errors:
		if (error) 
		{
			return console.warn(error);
		}
		
		// Store our int_mktcollectdtls info
		dondash.data.ymCollectDtlData = ymCollectDtlData;
		
		//Make the filters and dimensions:
		// dondash.makeFilterandDimensions(locData);
		
		// Initialize map and mnu:
		dondash.initMenu();
		dondash.initMap(usMap, locNames);
		
		// Trigger update with full dataset:
		dondash.onDataChange();
	}
}(window.dondash = window.dondash || {}));