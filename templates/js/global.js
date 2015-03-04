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
	function TriggerCat(cid) {
		var cat = $("div#cat.catid-"+cid);
		cat.children(".cbody").fadeToggle(500);
		cat.children(".cfoot").fadeToggle(500);
		setTimeout(function(){ cat.toggleClass("closed"); }, 500);
	}
	$("div#cat>div.cname>a.togglecat").on("click", function(){
		cid = $(this).parent().parent().attr('class').substring(6).split(" ")[0]
		TriggerCat(cid);
	});
});
