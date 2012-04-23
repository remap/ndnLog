 
$(document).ready(function(){
   setInterval ( "loadData()", 1000 );
 });



function loadData() {   
    var xobj = new XMLHttpRequest();
    xobj.overrideMimeType("application/json");
    xobj.open('GET', 'http://avatari.org/ucla/ndnlog/database.py/getLastForEachHost', true);
    xobj.onreadystatechange = function () {
        if (xobj.readyState == 4) {
            var jsonData = xobj.responseText;
            processData(jsonData);
        }
    }
    xobj.send(null);
}


function processData(data){
	if(data != ""){
		allData = "";
		var status = eval('(' + data + ')');
		// data obj/index order is : HOST | TIME | coRX | intTX
		var len=data.length;
		for(var i=0; i<len; i++) {
			var val = data[i];
			//alert('processing for '+val)
			allData+=makeDivForHost(val)
		}
		//alert(allData)
		//$(data).html(allData);
		document.getElementById("data").innerHTML=allData;
		// instead of status plot, would be nice to get a nice graph a la http://mbostock.github.com/d3/ex/stream.html
	}
}

function makeDivForHost(host){

div = '<div id="'+host[0]+'" class="data">';
div += "host: "+host[0]+"<br>";
div += " time: "+host[1];
div += " Content Objects: "+host[2];
div += " InterestPackets: "+host[3];
div += "<p></p></div>"

return div;
}