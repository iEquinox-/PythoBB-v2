jQuery(document).ready(function($){
	var id = 1,
		url = "http://127.0.0.1:8000";
		
	if(getCookie("catClosed") != null){ var cookieArray = getCookie("catClosed").split(",")
	} else { document.cookie = ("catClosed=; path=/"); var cookieArray = getCookie("catClosed").split(","); }
	if(getCookie("allowAlerts") == null) { document.cookie = ("allowAlerts=True;path=/") }
		
	function doRedirect(directory, time) {
		setTimeout(function(){
			location.href = url + directory
		}, time);
	}
		
	/* Cookie function: https://docs.djangoproject.com/en/dev/ref/csrf/ */
	function getCookie(name) {
		var cookieValue = null;
		if( document.cookie && document.cookie != '' ) {
			var cookies = document.cookie.split(';');
			for (var i = 0; i < cookies.length; i++ ) {
				var cookie = jQuery.trim(cookies[i]);
				if (cookie.substring(0,name.length+1)==(name+'=')) {
					cookieValue = decodeURIComponent(cookie.substring(name.length+1));
					break;
				}
			}
		}
		return cookieValue;
	}
	/* End Cookie function */
	function SendAlert(string) {
		var alert_content = "<div class=\"part-left\">!</div><div class=\"part-right\">" + string + "</div></div>";
		if( getCookie("allowAlerts") == "True" ) {
			if( $("div#alert").length ) {
				if( $("div#alert").length < 5 ) {
					$("div#alert").animate({marginBottom:"+=40px"}, 500)
					$("body").append("<div id=\"alert\" class=\"alertid-" + id + "\"px;\">" + alert_content);
				}
			} else {
				$("body").append("<div id=\"alert\" class=\"alertid-" + id + "\">" + alert_content);
			}
			var alert = $("div#alert.alertid-"+id);
			alert.slideDown(500); id += 1;
			setTimeout(function(){
				alert.slideUp(500);
				setTimeout(function(){
					alert.remove()
				},500);
				id -= 1;
			}, 5000);
		}
	}
	function TriggerCat(cid, full) {
		var cat = $("div#cat.catid-"+cid);
		var head = cat.children(".cname");
		if(full == false){
			cat.children(".catbody").slideToggle(500);
			setTimeout(function(){
				cat.toggleClass("closed");
				if( cat.hasClass("closed") ){
					cookieArray.push(cid);
					document.cookie = ("catClosed=" + cookieArray.join() + ";");
				} else {
					cookieArray.splice(cookieArray.indexOf(cid),1);
					document.cookie = ("catClosed=" + cookieArray.join() + ";");
				}
			}, 500);
		} else {
			cat.toggleClass("closed");
			if( cat.hasClass("closed") ){
					cookieArray.push(cid);
					document.cookie = ("catClosed=" + cookieArray.join() + ";")
			} else {
					cookieArray.splice(cookieArray.indexOf(cid),1)
					document.cookie = ("catClosed=" + cookieArray.join() + ";")
			}
		}
	}
	
	$("input.check_credentials").on("click", function(){
		if( $("input.username.required").val() == "" || $("input.password.required").val() == "" ) {
			$("input.check_credentials").prop('disabled', true);
			SendAlert('Both username and password fields must be filled in.');
			setTimeout(function(){
				$("input.check_credentials").prop('disabled', false);
			}, 100);
		}
	});
	
	$("form.state-form").submit(function(event){
		event.preventDefault();
		if( $(this).hasClass("login") ) {
			if( $("input.username.required").val() != "" || $("input.password.required").val() != "" ) {
				var action = $(this).attr("action");
				$.ajax({type:"POST", url: action, data: {csrfmiddlewaretoken:getCookie("csrftoken"), Username:$("input.username.required").val(), Password:$("input.password.required").val()}, dataType: "json",
					success: function(data) {
						if(data.LoginAttempt === false) {
							SendAlert("Wrong username or password.");
						} else {
							SendAlert("Login successful. Redirecting.");
							document.cookie = ("sid="+data.LoginAttempt+"; path=/");
							doRedirect("/",1000);
						}
					}, error: function(jqXHR, textStatus, error){
						sendAlert("An error has occured. Please contact the forum administrator.");
						console.log(textStatus);
						console.log(error);
					}
				});
			}
		} else if( $(this).hasClass("register") ) {
			if( $("input.username.required").val() == "" || $("input.password.required").val() == "" || $("input.passwordre.required").val() == "" || $("input.email.required").val() == "" ) {
				SendAlert("Missing input.");
			} else {
				var action = $(this).attr("action");
				if( $("input.password.required").val() == $("input.passwordre.required").val() ) {
					$.ajax({type:"POST", url: action,
						data: {
							csrfmiddlewaretoken:getCookie("csrftoken"),
							Username:$("input.username.required").val(),
							Password:$("input.password.required").val(),
							Email:$("input.email.required").val()},
							dataType:"json",
							success: function(data) {
								console.log(data);
								if (data.RegisterAttempt.register == true) {
									SendAlert(data.RegisterAttempt.message);
									document.cookie = "sid=" + data.RegisterAttempt.sid + "; path=/"
									doRedirect("/", 1000)
								} else {
									SendAlert(data.RegisterAttempt.message);
								}
							},
							error: function(jqXHR, textStatus, error){
								SendAlert("An error has occured. Please contact the forum administrator.");
								console.log(textStatus);
								console.log(error);
							}
						});
				} else {
					SendAlert("Passwords do not match.");
				}
			}
		}		
	});
	
	// $("input.CSRFToken").attr('value', getCookie("csrftoken"));

	$("a.javascript.dologout").on("click", function(){
		SendAlert("Logout successful.");
		document.cookie = "sid=; path=/"
		doRedirect("/", 1000);
	});
	
	for(var c in cookieArray){
		$("div#cat.catid-"+c).addClass("closed")
	}	
	
	$("div#cat>div.cname>a.togglecat").on("click", function(){
		cid = $(this).parent().parent().attr('class').substring(6).split(" ")[0]
		TriggerCat(cid, false);
		SendAlert('Category toggled.')
	});
});
