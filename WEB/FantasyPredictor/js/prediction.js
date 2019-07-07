
function myFunction() {
  document.getElementById("myDropdown").classList.toggle("show");
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


function loadFunction(){
  var url = window.location.pathname;
  var filename = url.substring(url.lastIndexOf('/')+1);
  filename = filename.substring(0, filename.lastIndexOf('.'))

    //document.getElementById("gameweek").innerHTML = "Gameweek "+filename;
    document.getElementById("mainTitle1").innerHTML = "Gameweek "+filename;

  getPrediction(filename);
}

async function getPrediction(gameweek){
  try{
  const response = await fetch('http://localhost:5000/predict/'+gameweek, {
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
  for (i = 0; i < data.goalkeepers.length; i++) {
    goalkeepers.push(data.goalkeepers[i].name)
    points += data.goalkeepers[i].points
  }

  var defenders = []
  for (i = 0; i < data.defenders.length; i++) {
    defenders.push(data.defenders[i].name)
    points += data.defenders[i].points
  }

  var midfielders = []
  for (i = 0; i < data.midfielders.length; i++) {
    midfielders.push(data.midfielders[i].name)
    points += data.midfielders[i].points
  }


  var forwards = []
  for (i = 0; i < data.forwards.length; i++) {
    forwards.push(data.forwards[i].name)
    points += data.forwards[i].points
  }
  document.getElementById("mainTitle2").innerHTML = ""
  document.getElementById("goalkeepers").innerHTML = goalkeepers
  document.getElementById("defenders").innerHTML = defenders
  document.getElementById("midfielders").innerHTML = midfielders
  document.getElementById("forwards").innerHTML = forwards
  document.getElementById("points").innerHTML = "Total Points: "+points
  return -1
}
