function Tester() {
	this.baseUrl = 'https://iiif.io/api/image/validator/service/';
	
	this.categories = {
		1: 'Info/Identifier',
		2: 'Region',
		3: 'Size',
		4: 'Rotation',
		5: 'Quality',
		6: 'Format',
		7: 'HTTP'
	};

	this.tests = {};
	this.currentTests = [];
	this.cancelled = false;
}

Tester.prototype.doLevelCheck = function(level) {
	for (var t in this.tests) {
		var test = this.tests[t];
		$('#'+t).prop('checked', test.level <= level);
	}
};

Tester.prototype.showMessage = function(title, msg) {
	$('#dialog').dialog('option', 'title', title);
	$('#dialog p').html(msg);
	$('#dialog').dialog('open');
};

Tester.prototype.fetchTestList = function() {
	var _this = this;
	var testContainer = $('#tests > div');
	testContainer.empty();
	for (var c in this.categories) {
		var name = this.categories[c];
		testContainer.append('<div id="c_'+c+'" class="category"><h2>'+name+'</h2></div>');
	}

	$.ajax({
		url: this.baseUrl+"list_tests",
		data: {
			version: $("#version").val(),
			t: new Date().getTime()
		},
		dataType: 'json',
		success: function(data, status, xhr) {

			_this.tests = data;

			ltests = [];
			for (var t in data) {
				if (data.hasOwnProperty(t)) {
					test = data[t];
					test.id = t;
					ltests.push(test);
				}
			}
			ltests.sort(function(a,b) {return a.level - b.level});

			// sort tests by level

			for (var t=0, test; test = ltests[t]; t++) {
				var label = test.label || test.id;
				$('#c_'+test.category).append('<div class="input">'+
					'<input id="'+test.id+'" type="checkbox" name="'+test.id+'"/><label for="'+test.id+'">'+label+'</label>'+
				'</div>');
			}
			$('#tests input').click(function(ev) {
				$('#level').val('-1');
			});
			$('#level').val('1');
			_this.doLevelCheck(1);
		}
	});
}

Tester.prototype.init = function() {

	this.fetchTestList();

	$('#dialog').dialog({
		autoOpen: false,
		modal: true,
		height: 250,
		width: 270,
		buttons: {
			Ok: function() {
				$(this).dialog('close');
			}
		}
	});

	$('#inputs ins').each(function(index, el) {
		var msg = '';
		switch (index) {
			case 0:
				msg = 'The base URI for your IIIF implementation, e.g. <span class="code">http://shared-canvas.org</span>.';
				break;
			case 1:
				msg = 'The prefix for your IIIF implementation, e.g. <span class="code">iiif</span>.';
				break;
			case 2:
				msg = 'The filename for a test image you generated from the "Generate Test Image" tab and saved to your server. Leave off the <span class="code">.png</span> extension. The ID should look something like: <span class="code">f8c6e480-f75d-11e1-b397-0011259ed879</span>';
		}
		$(el).data('msg', msg);
	}).click($.proxy(function(ev) {
		this.showMessage('Help', $(ev.target).data('msg'));
	}, this));

	$('#level').change($.proxy(function(ev) {
		var level = parseInt($(ev.target).val());
		this.doLevelCheck(level);
	}, this));

	$('#version').change($.proxy(function(ev) {
		// regenerate test options
		this.fetchTestList();
	}, this));

	$('#run_tests').click($.proxy(function(ev) {
		var errors = '';

		var uri = $('#server').val();
		if (uri == '') {
			errors += 'The Server field is empty.\n';
		}

		var prefix = $('#prefix').val();
		if (prefix == '') {
			errors += 'The Prefix field is empty.\n';
		}

		var id = $('#identifier').val();
		if (errors == '') {
			$('#tabs').hide();
			$('#results').show();
			this.runTests(uri, prefix, id);
		} else {
			this.showMessage('Error', errors);
		}

	}, this));

};

$(document).ready(function() {
	tester = new Tester();
	tester.init();
});
