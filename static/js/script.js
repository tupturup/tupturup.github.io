$(function() {
	var submit_form = function(e) {
		$.getJSON(
			//url - A string containing the URL to which the request is sent.
			$SCRIPT_ROOT+'/add',
			//data - A plain object or string that is sent to the server with the request.
			{
				first_name: $('input[name="first_name"]').val(),
				last_name: $('input[name="last_name"]').val(),
				email: $('input[name="email"]').val(),
				age: $('input [name="age"]').val()
			},
			//success - A callback function that is executed if the request succeeds.
			function(data) {
				$('input[name=name]').focus().select();
			});
			return false;
		};

		$('button#calculate').click(submit_form);
		$('input[type=text]').keydown(function(e) {
			if (e.keyCode == 13) {
				submit_form(e);
			}
		});
		$('input[name="first_name"]').focus();
});
