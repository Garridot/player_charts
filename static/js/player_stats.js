function getCookie(name) {  
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {                
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {                    
          const cookie = cookies[i].trim();
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {                        
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}

  
  
const playername = String(player).split(' ');  
  
  
  // Get name player 
const getName = (playername)=>{
  if(playername.length == 1){
    var name = playername;
  } 
  else{
    var name = playername[1];
  }

  return String(name)
}



var maintext = document.querySelectorAll(".main-text .playername h1");   

maintext.forEach(i=>{
    i.innerHTML = getName(playername);
})
  
  
  
  
  
  //// CHARTS ////
  
  
  
function getRequest(player){  

  
  var player = String(player).replace(" ","%20");

  
  
  var select = document.querySelector('.teams-filter select');
  var team = select.options[select.selectedIndex].value;    
  
  
  getgeneralStats(player,team);
  getcareerGames(player,team);
  getrateGoals(player,team);
  getgoalsbySeason(player,team);
  getperformanceCompetition(player,team); 
}





// 


function getgeneralStats(player,team){  
  // fetch( `https://football-player-charts.onrender.com/general_stats/${player}/${team}` ,{ 
  fetch( `/general_stats/${player}/${team}` ,{ 
    method:'POST',
    headers:{
        'Content-Type':'application/json',                
        'X-CSRFToken' : getCookie('csrftoken')          
    },             
    })    
    .then((response)=>{ return response.json();}) 
    .then(result => {
      let table =  document.querySelector('.list-general');   
      
      table.innerHTML =  `
        <li>
          <h2>Matches: ${result.Matches}</h2> 
        </li>   
        <li>
          <h2>Goals: ${result.Goals} </h2><h5>(${result.Ratio_gls} per game)</h5> 
        </li>
        <li>
          <h2>Assits: ${result.Assists}</h2> <h5>(${result.Ratio_ass} per game)
        </li>                                 
      `
      
    })         
}


function getcareerGames(player,team){
  fetch( `/career_games/${player}/${team}` ,{  
    method:'POST',            	 
    headers:{
        'Content-Type':'application/json',                
        'X-CSRFToken' : getCookie('csrftoken') ,
    }, 
    
  })
  .then((response)=>{ return response.json();}) 
  .then(result => {    
    var res = result;

    var games = document.querySelectorAll(".games-data span:nth-child(1)");

    for (let i = 0; i < games.length; i++) {
      games[0].innerHTML = res.games;
      games[1].innerHTML = res.wins;
      games[2].innerHTML = res.draws;
      games[3].innerHTML = res.defeats;
      
    }
  })
}







function getrateGoals(player,team){  
  fetch( `/goals_involvements_rate/${player}/${team}` ,{  
    method:'POST',            	 
    headers:{
        'Content-Type':'application/json',                
        'X-CSRFToken' : getCookie('csrftoken') ,
    }, 
    
  })
  .then((response)=>{ return response.json();}) 
  .then(result => {
      var data = result;  
      
      var listgoals = document.querySelectorAll(".players-goals .list-goals h2:nth-child(2)");
      for (let i = 0; i < listgoals.length; i++){
        listgoals[0].innerHTML = data.team_goals;
        listgoals[1].innerHTML = data.player_goals;
        listgoals[2].innerHTML = data.player_assists;
        listgoals[3].innerHTML = data.rate_goals_involvements+ "%";
      }

      document.querySelector(".donut-table p").innerHTML =  data.rate_goals_involvements+ "%";

      DonutChart(data);
      
  })         
}
let goalsChart; 
const DonutChart = (data)=>{

  var homedonut = {
    labels: [ "Player's Goals","Player's Assists", "Teams's Goals" ],
    datasets: [
      {        
        data: [data.player_goals,data.player_assists,data.team_goals - (data.player_goals + data.player_assists)],
        label: "player's Goals",
        borderWidth: 0,
        backgroundColor: [
          "#c7c7c7",
          "#720303",
          "#0c0c12",
        ],  
    }]
  };

  var goals   = document.querySelector("#goals_donut").getContext('2d') ;

  if (goalsChart) {
    goalsChart.destroy();        
  }

  goalsChart = new Chart(goals, {
      type: 'doughnut',
      data: homedonut,    
      options: {            
        cutout: '90%',   
        plugins: {          
          legend: {      
            display: false,            
          },
          responsive: true,      
        },
      } 
  });
}





function getgoalsbySeason(player,team){
  fetch( `/goals_involvements_season/${player}/${team}` ,{                            
          method:'POST',            
          headers:{
              'Content-Type':'application/json',                
              'X-CSRFToken' : getCookie('csrftoken')          
          }, 
      })
  .then((response)=>{ return response.json();}) 
  .then(result => {
      var res = result
      
      goalsbyseasonChart(res)
  })
}


let linechart
const goalsbyseasonChart = (res)=>{    

  var ctx = document.querySelector('#line_season').getContext('2d')

  if (linechart) {
      linechart.destroy();
  }

  if(res.Seasons.length >= 2){   

    var dataline =  {
      labels : res.Seasons,
      datasets:[            
          {
              label : 'Goals',
              data  : res.Goals,
              fill: 'start',  
              borderColor: '#720303', 
              pointBackgroundColor: 'white',
              borderWidth: .5,
              tension: 0.1,
              
          },
          {
              label : 'Assists',
              data  : res.Assists,
              fill: 'start',
              borderColor: '#30dde7',
              pointBackgroundColor: '#aaa',
              borderWidth: .2,
              tension: 0.1,
              
          },                
          {
              label : 'Goals involvements',
              data: res.goals_involvements,
              fill: 'start',                    
              borderColor: '#cedddd',
              pointBackgroundColor: '#cedddd',
              borderWidth: .5,
              tension: 0.1,              
              
          },
          {
              label : "Games",
              data: res.Games,
              fill: 'start',                                      
              backgroundColor:"#0c0c12",                        
              type: 'bar',
          },       
  ]
    }
      
    linechart = new Chart(ctx,{                             
            
      type: "line",
        data: dataline,
        options: {                    
          maintainAspectRatio: false,              
          responsive: true,
          interaction: {
             mode: 'index',
            intersect: true,
          },      
          plugins: { 
            legend: {                
              display:true,                
              labels: {
                color: '#adadad',                                                 
              },                                                            
            },              
          }             
        }  
    })   
  }else{
      document.querySelector('.gls_by_seassons').style.display = 'none'
  } 
}





function getperformanceCompetition(path,team){
  fetch( `/performance_competition/${path}/${team}` ,{                            
      method:'POST',         
      headers:{
          'Content-Type':'application/json',                
          'X-CSRFToken' : getCookie('csrftoken')          
      }, 
  })
  .then((response)=>{ return response.json();}) 
  .then(result => {
      var res = result       
      

      let table =  document.querySelector('.performance-data')
        
      while (table.hasChildNodes()){                
          table.removeChild(table.lastChild);}
      
      for (i in res.Competition){
        var performace = document.createElement("ul");
        performace.className = "performace";

        performace.innerHTML =  `
                    <li class="table-data">${res.Competition[i]}</li>
                    <li class="table-data">${res.games[i]}</li>
                    <li class="table-data">${res.team_goals[i]}</li>
                    <li class="table-data">${res.goals[i]}</li>
                    <li class="table-data">${res.assists[i]}</li>
                    <li class="table-data">${res.performance[i]}%</li>
        `


        table.appendChild(performace)
      }
          
  })
}

getRequest(player)  
