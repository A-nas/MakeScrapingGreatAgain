</script>
function DateFormat(x,currentYear = "2017",currentMonth = "nov.", currentDay = "11" ){
	var months = {"janv.": "jan", "janv.": "jan", "févr": "feb", "févr." : "feb", "mars" : "mar", "mars." : "mar", "avr" : "apr", "avr." : "apr", "mai" : "may", "mai." : "may", "juin" : "jun", "juin." : "jun", "juil" : "jul", "juil." : "jul", "août" : "aug", "août." : "aug", "sept" : "sep", "sept." : "sep", "oct" : "oct", "oct." : "oct", "nov" : "nov", "nov." : "nov", "déc" : "dec", "déc." : "dec"};
	var newDateArray = x.split(" ");
	if (newDateArray.length == 2){
		return currentYear +"-"+ months[newDateArray[1]] +"-"+ newDateArray[0];
	}else if(newDateArray.length == 3){
		return newDateArray[2] +"-"+ months[newDateArray[1]] +"-"+ newDateArray[0];
	}else if(newDateArray.length == 1){
	    return currentYear +"-"+ months[currentMonth] +"-"+ currentDay;
	}else{
		return x;
	}
}
<script>