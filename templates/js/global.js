jQuery(document).ready(function($){
	var id = 1,
		cookieArray = getCookie("catClosed").split(",");
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
					$("body").append("<div id=\"alert\" class=\"alertid-" + id + "\" style=\"margin-bottom:" + 50 * $("div#alert").length + "px;\">" + alert_content);
				}
			} else {
				$("body").append("<div id=\"alert\" class=\"alertid-" + id + "\">" + alert_content);
			}
			var alert = $("div#alert.alertid-"+id);
			alert.fadeIn(500); id += 1;
			setTimeout(function(){
				alert.fadeOut(500);
				setTimeout(function(){
					alert.remove()
				},500);
				id -= 1;
			}, 5000);
		}
	}
	function TriggerCat(cid, full) {
		var cat = $("div#cat.catid-"+cid);
		if(full == false){
			cat.children(".cbody").fadeToggle(500); cat.children(".cfoot").fadeToggle(500);
			setTimeout(function(){
				cat.toggleClass("closed");
				if( cat.hasClass("closed") ){
						cookieArray.push(cid);
						document.cookie = ("catClosed=" + cookieArray.join() + ";")
				} else {
						cookieArray.splice(cookieArray.indexOf(cid),1)
						document.cookie = ("catClosed=" + cookieArray.join() + ";")
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

	
	for(var c in cookieArray){
		$("div#cat.catid-"+c).addClass("closed")
	}	
	
	$("div#cat>div.cname>a.togglecat").on("click", function(){
		cid = $(this).parent().parent().attr('class').substring(6).split(" ")[0]
		TriggerCat(cid, false);
		SendAlert('Category toggled.')
	});
});
