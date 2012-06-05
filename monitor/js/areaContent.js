var labelType, useGradients, nativeTextSupport, animate, areaChart, json;

$(document).ready(function(){
	json = "";
	loadData()
   setInterval ( "loadData()", 4000 );
 });


function loadData() {   
    var xobj = new XMLHttpRequest();
    xobj.overrideMimeType("application/json");
    xobj.open('GET', 'http://borges.metwi.ucla.edu/ec2/ndnLog/database.py/getCOForAreaChartDynamicHostname', true);
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
		if(json == ""){
			json = eval('(' + data + ')');
			init(json)
		} else {
		json = eval('(' + data + ')');
		//areaChart.canvas.clear()jit
		//areaChart.updateJSON(json);
		areaChart.loadJSON(json);
		drawLegend()
		//init(json)
		}
	}
}



(function() {
  var ua = navigator.userAgent,
      iStuff = ua.match(/iPhone/i) || ua.match(/iPad/i),
      typeOfCanvas = typeof HTMLCanvasElement,
      nativeCanvasSupport = (typeOfCanvas == 'object' || typeOfCanvas == 'function'),
      textSupport = nativeCanvasSupport 
        && (typeof document.createElement('canvas').getContext('2d').fillText == 'function');
  //I'm setting this based on the fact that ExCanvas provides text support for IE
  //and that as of today iPhone/iPad current text support is lame
  labelType = (!nativeCanvasSupport || (textSupport && !iStuff))? 'Native' : 'HTML';
  nativeTextSupport = labelType == 'Native';
  useGradients = nativeCanvasSupport;
  animate = !(iStuff || !nativeCanvasSupport);
})();

var Log = {
  elem: false,
  write: function(text){
    if (!this.elem) 
      this.elem = document.getElementById('log');
    this.elem.innerHTML = text;
    this.elem.style.left = (500 - this.elem.offsetWidth / 2) + 'px';
  }
};


function init(json){
    //init data
    var infovis = document.getElementById('infovis');
    //init AreaChart
   	areaChart = new $jit.AreaChart({
      //id of the visualization container
      injectInto: 'infovis',
      //add animations
      animate: false,
      //separation offsets
      Margin: {
        top: 5,
        left: 5,
        right: 5,
        bottom: 5
      },
      labelOffset: 10,
      //whether to display sums
      showAggregates: false,
      //whether to display labels at all
      showLabels: false,
      //could also be 'stacked'
      type: useGradients? 'stacked:gradient' : 'stacked',
      //label styling
      Label: {
        type: labelType, //can be 'Native' or 'HTML'
        size: 13,
        family: 'Arial',
        color: 'white'
      },
      //enable tips
      Tips: {
        enable: true,
        onShow: function(tip, elem) {
          tip.innerHTML = "<b>" + elem.name + "</b>: " + elem.value;
        }
      },
      //add left and right click handlers
      filterOnClick: true,
      restoreOnRightClick:true
    });
    //load JSON data.
    areaChart.loadJSON(json);
    //end
    var button = $jit.id('update'),
        restoreButton = $jit.id('restore');

    //restore graph on click
    $jit.util.addEvent(restoreButton, 'click', function() {
      areaChart.restore();
    });
	drawLegend()
}

function drawLegend(){
 var list = $jit.id('id-list')
    //dynamically add legend to list
    var legend = areaChart.getLegend(),
        listItems = [];
    for(var name in legend) {
      listItems.push('<div class=\'query-color\' style=\'background-color:'
          + legend[name] +'\'>&nbsp;</div>' + name);
    }
    listItems.reverse();
    list.innerHTML = '<li>' + listItems.join('</li><li>') + '</li>';
}
