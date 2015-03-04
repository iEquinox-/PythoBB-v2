jQuery(document).ready(function($){
	var id = 1;
	function SendAlert(string) {
		$("body").append("<div id=\"alert\" class=\"alertid-" + id + "\"><div class=\"part-left\">!</div><div class=\"part-right\">" + string + "</div></div>");
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
});
