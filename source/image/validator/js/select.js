function Tester() {
	this.baseUrl = 'https://image-validator.iiif.io/';
	
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

	$("#dialog").dialog({
		autoOpen: false,
		modal: true,
		height: 400,
		width: "50%",
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
				msg = "The base URI for your IIIF implementation. For example if the path to your info.json was: <br/><br/>https://iiif.io/api/image/3.0/example/reference/f8c6e480-f75d-11e1-b397-0011259ed879/info.json <br/><br/> the Server would be <span class=\"code\">https://iiif.io</span>.";
				break;
			case 1:
				msg = "The prefix for your IIIF implementation. For example if the path to your info.json was <br/><br/>https://iiif.io/api/image/3.0/example/reference/f8c6e480-f75d-11e1-b397-0011259ed879/info.json<br/><br/> the Prefix would be <span class=\"code\">/api/image/3.0/example/reference/</span>.";
				break;
			case 2:
				msg = "The filename for a test image you generated from the \"Generate Test Image\" tab and saved to your server. Leave off the <span class=\"code\">.png</span> extension. For example if the path to your info.json was <br/><br/>https://iiif.io/api/image/3.0/example/reference/f8c6e480-f75d-11e1-b397-0011259ed879/info.json<br/><br/> the Image ID would be: <span class=\"code\">f8c6e480-f75d-11e1-b397-0011259ed879</span>";
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
			errors += '<li>The Server field is empty.</li>\n';
		}

		var prefix = $('#prefix').val();
		if (prefix == '') {
			errors += '<li>The Prefix field is empty.</li>\n';
		}

		var id = $('#identifier').val();
		if (errors == '') {
			$('#tabs').hide();
			$('#results').show();
			this.runTests(uri, prefix, id);
		} else {
            ev.preventDefault();
			this.showMessage('Missing required fields',"<ul>" + errors + "</ul>");
		}

	}, this));

};

document.addEventListener("DOMContentLoaded", function(event) {
    $.getScript("https://code.jquery.com/ui/1.12.1/jquery-ui.min.js", function(data, textStatus, jqxhr) {
      tester = new Tester();
      tester.init();
    });
});
