var done = function(res, status) {
	if (status == "success") {
		var text = res.responseText;
		var obj = $.parseJSON(text);
		
		//TODO: error checking with hasOwnProperty?
		if (obj.result == "match") {
			$("#resultsStatus").append('Found a match!');
		}
		else if (obj.result == "loop") {
			$("#resultsStatus").append('Went into an infinite loop!');			
		}
		else if (obj.result == "dead_end") {
			$("#resultsStatus").append('Reached a dead end!');
		}
		else if (obj.result == "error") {
			$("#resultsStatus").append('Ran into an error, oops!');
		}
			
		for (var i = 0; i < obj.articles.length; i++) {
			var artHtml = $("<li>" + obj.articles[i] + "</li>");
			$("#results").append(artHtml);
		}
	}
	else {
		alert("Error");
	}
};

var fetch_road = function() {
	$("#resultsStatus").empty();
	$("#results").empty();
	
	var article = $("#inpArt").val();
	if (article != "") {
		var data = { article:article };
		var args = { type:"POST", url:"/fetch/", data:data, complete:done };
		$.ajax(args);
	}
};

$("#submitBtn").click(fetch_road);