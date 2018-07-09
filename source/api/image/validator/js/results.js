


function Tester() {
	this.baseUrl = 'https://iiif.io/api/image/validator/service/';

	this.categories = {
		1: 'Info/Identifier',
		2: 'Region',
		3: 'Size',
		4: 'Rotation',
		5: 'Quality',
		6: 'Format'
	};

	this.tests = {};
	this.currentTests = [];
	this.cancelled = false;
}

Tester.prototype.getQueryParams = function () {
    var match,
        pl     = /\+/g,  // Regex for replacing addition symbol with a space
        search = /([^&=]+)=?([^&]*)/g,
        decode = function (s) { return decodeURIComponent(s.replace(pl, " ")); },
        query  = window.location.search.substring(1),
		urlParams = {};

    while (match = search.exec(query))
       urlParams[decode(match[1])] = decode(match[2]);

   	return urlParams;
}


Tester.prototype.runTests = function(uri, prefix, imageId, version) {
	this.cancelled = false;
	var totalTests = this.currentTests.length;
	var testsPassed = 0;

	$('#results h1').html('Results');

	var resultsContainer = $('#results');
	resultsContainer.empty();

	for (var i = 0; i < this.currentTests.length; i++) {
		var t = this.currentTests[i];
		//var test = this.tests[t];
		//var label = test.label || t;
		resultsContainer.append('<div id="r_'+t+'" class="result ui-corner-all">'+
			'<span class="resultLabel">'+ t +'</span><span class="elapsed"></span><span class="message"></span>'+
		'</div>');
	}

	function doTest(test) {
		if (test) {
			var testStart = new Date().getTime();
			$.ajax({
				url: this.baseUrl+test,
				data: {
					version: version,
					server: uri,
					prefix: prefix,
					identifier: imageId,
					t: testStart
				},
				dataType: 'json',
				success: $.proxy(function(data, status, xhr) {
					var testFinish = new Date().getTime();
					var result = $('#r_'+test);
					var elapsed = testFinish - testStart;
					result.find('.elapsed').html('Elapsed time (ms): '+elapsed);
					result.find('.resultLabel').html(data.label);

					var message = '<ul>';
					if (data.status) {
						if (data.status == 'success') {
							result.addClass('pass');
							testsPassed++;
						} else {
							result.addClass('fail');
						}
						for (var key in data) {
							if (key != 'status' && key != 'test' && key != 'label') {
								message += '<li>'+key+': '+data[key]+'</li>';
							}
						}
					} else {
						result.addClass('fail');
						message = '<li>Message: '+status+'</li>';
					}
					message += '</ul>';
					result.find('.message').html(message);

					$.proxy(doTest, this)(this.currentTests.shift());
				}, this),
				error: $.proxy(function(xhr, status, error) {
					var testFinish = new Date().getTime();
					var result = $('#r_'+test);
					var elapsed = testFinish - testStart;

					result.find('.elapsed').html('Elapsed time (ms): '+elapsed);
					result.addClass('fail');
					var message = '<ul><li>Message: '+status+'</li></ul>';
					result.find('.message').html(message);

					$.proxy(doTest, this)(this.currentTests.shift());
				}, this)
			});
		} else {
			if (!this.cancelled) {
				var details = '<br/> '+testsPassed+' out of '+totalTests+' tests passed.';
				var result;
				if (testsPassed == totalTests) {
					result = 'passed';
					$('#results h1').append(': Pass'+details);
				} else {
					result = 'failed';
					$('#results h1').append(': Fail'+details);
				}
				var level = $('#level').val();
				if (level == '-1') level = 'Custom';
				var msg = 'You '+result+' IIIF Compliance Level: '+level+'.'+details;
				// this.showMessage('Result', msg);
			}
		}
	}

	$.proxy(doTest, this)(this.currentTests.shift());
};

Tester.prototype.cancelTests = function() {
	this.currentTests = [];
	this.cancelled = true;
};

Tester.prototype.init = function() {

	// Get tests and data from query
	var params = this.getQueryParams();
	var server = params['server'],
	    prefix = params['prefix'],
	    id = params['identifier'],
	    version = params['version'],
	    tests = [];

	for (var key in params) {
		if (params.hasOwnProperty(key) && params[key] == "on") {
			tests.push(key);
		}
	}
	this.currentTests = tests;
	this.runTests(server, prefix, id, version);
};

$(document).ready(function() {
	tester = new Tester();
	tester.init();
});
