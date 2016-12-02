var DyadControl = L.Control.extend({
	initialize: function (name, options) {
    	L.Util.setOptions(this, options);
    },
		
		//function to be called when the control is added to the map
    onAdd: function (map) {
			
			//create the control container with a 
			//class name
        var container = L.DomUtil.create('div', 'dyad-control');
			
		
		$.getJSON("http://localhost:5000/dyads", 
			function(data) {
				var temp = data.result	
					
					var dyad_select = document.createElement('select');
					dyad_select.id = name; 
					dyad_select.onchange = update; 
					$.each(temp, function(i,item){
						dyad_select[dyad_select.length] = new Option(item, i, false, false);
					});
					container.appendChild(dyad_select); // myDiv i

				
	    			container.firstChild.onmousedown = 
					container.firstChild.ondblclick = 
					L.DomEvent.stopPropagation;
							
			});
			
		return container;
			
	}
});

function update(){
   		console.log("debug");
}