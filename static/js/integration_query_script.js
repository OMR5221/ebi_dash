// URL Port our api is running from:
var API_URL = 'http://127.0.0.1:5000/api'

var displayJSON = function(query)
{
	d3.json(API_URL + query, function(error, data)
	{
		// log error to console
		if(error)
		{
			return console.warn(error)
		}
	
		// select pre tags and fill with the query string
		d3.select('#query pre').html(query);
		// and fill with the converted JSON data from the server
		d3.select('#data pre').html(JSON.stringify(data, null, 4));
		console.log(data);
	});
};

var filters = [
	{"name": "CollectionDateSK", "op": "gte", "val": 20180324},
	{"name": "CompletedFlag", "op": "gte", "val": 8}
];

var order_by = [{"field": "CollectionDateSK", "direction": "asc"}]

var query = '/INT_MKTCollectionDetails?' + 'q=' + JSON.stringify(
{
	'filters': filters,
	'order_by':order_by
});

//Run function with out query
displayJSON(query)