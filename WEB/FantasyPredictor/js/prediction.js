
function myFunction() {
  document.getElementById("myDropdown").classList.toggle("show");
}

function testFunction(){
  console.log("IN javascript TestFunction()")
}

// Close the dropdown if the user clicks outside of it
window.onclick = function(event) {
  if (!event.target.matches('.dropbtn')) {
    var dropdowns = document.getElementsByClassName("dropdown-content");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
      }
    }
  }
}


function loadFunction(model){

  var url = window.location.pathname;
  var filename = url.substring(url.lastIndexOf('/')+1);
  filename = filename.substring(0, filename.lastIndexOf('.'))

    //document.getElementById("gameweek").innerHTML = "Gameweek "+filename;
    document.getElementById("mainTitle1").innerHTML = "Gameweek "+filename;

  getPrediction(filename, model);
}

async function getPrediction(gameweek, model){
  try{
  const response = await fetch('http://localhost:5000/predict/'+gameweek+'/'+model, {
    method: 'GET',
    //body: myBody, // string or object
    headers: {
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin':'*'
    }
  })
  .then(res = async(res) => await res.json())//response type
  .then(data => {
    console.log("Got response..")
    return data
  }); //log the data;
  data = (await Promise.resolve(response))
  console.log(data)
}
catch(err){

  document.getElementById("mainTitle2").innerHTML = "Connection timed out"
  return -1
}

  var goalkeepers = []
  var points = 0
  for (i = 0; i < data[model].goalkeepers.length; i++) {
    goalkeepers.push(data[model].goalkeepers[i].name+" ("+data[model].goalkeepers[i].points+")")
    points += data[model].goalkeepers[i].points
  }

  var defenders = []
  for (i = 0; i < data[model].defenders.length; i++) {
    defenders.push(data[model].defenders[i].name+" ("+data[model].defenders[i].points+")")
    points += data[model].defenders[i].points
  }

  var midfielders = []
  for (i = 0; i < data[model].midfielders.length; i++) {
    midfielders.push(data[model].midfielders[i].name+" ("+data[model].midfielders[i].points+")")

    points += data[model].midfielders[i].points
  }


  var forwards = []
  for (i = 0; i < data[model].forwards.length; i++) {
    forwards.push(data[model].forwards[i].name+" ("+data[model].forwards[i].points+")")
    points += data[model].forwards[i].points
  }
  document.getElementById("mainTitle2").innerHTML = "Total Points: "+points

  document.getElementById("goalkeeper").innerHTML = goalkeepers

  for(i =1; i <= defenders.length; i++){
    var current = "defender"+[i]
    document.getElementById(current).innerHTML = defenders[i-1]
  }

  for(i =1; i <= midfielders.length; i++){
    var current = "midfielder"+[i]
    document.getElementById(current).innerHTML = midfielders[i-1]
  }

  document.getElementById("forward1").innerHTML = forwards
  //document.getElementById("points").innerHTML = "Total Points: "+points
  return -1
}
