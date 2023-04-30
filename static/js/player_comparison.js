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

function get_stats(first_player,second_player){   
    getStats(first_player,second_player);
    getSeasons(first_player,second_player);
    getStatsCompetition(first_player,second_player);     
}

const getStats = (first_player,second_player)=>{
    fetch( `/player_comparison/general_stats/${first_player}/${second_player}`,{ 
        headers:{
            'Content-Type':'application/json',                
            'X-CSRFToken' : getCookie('csrftoken')          
        },             
        })
    .then((response)=>{ return response.json();}) 
    .then(result => {
        var data = result;
        generalStats(data); 
         
    })
}
const generalStats = (data)=>{
    var stas1 = document.querySelectorAll(".stats-table ul li .row:nth-child(1) h1");
    var stas2 = document.querySelectorAll(".stats-table ul li .row:nth-child(3) h1");
    
    stas1[0].innerHTML =  data.player1.matches;
    stas2[0].innerHTML =  data.player2.matches;       

    stas1[1].innerHTML =  data.player1.goals;
    stas2[1].innerHTML =  data.player2.goals;        

    stas1[2].innerHTML =  data.player1.assists;
    stas2[2].innerHTML =  data.player2.assists;

    stas1[3].innerHTML =  data.player1.involvement+"%";
    stas2[3].innerHTML =  data.player2.involvement+"%";

    if(data.player1.matches>data.player2.matches){
        stas1[0].classList.add("greatest");
    }else{
        stas2[0].classList.add("greatest");
    } 

    if(data.player1.goals>data.player2.goals){
        stas1[1].classList.add("greatest");
    }else{
        stas2[1].classList.add("greatest");
    } 

    if(data.player1.assists>data.player2.assists){
        stas1[2].classList.add("greatest");
    }else{
        stas2[2].classList.add("greatest");
    } 
    if(data.player1.involvement>data.player2.involvement){
        stas1[3].classList.add("greatest");
    }else{
        stas2[3].classList.add("greatest");
    } 
}



const getSeasons = (first_player,second_player)=>{
    fetch( `/player_comparison/byseason/${first_player}/${second_player}`,{ 
        headers:{
            'Content-Type':'application/json',                
            'X-CSRFToken' : getCookie('csrftoken')          
        },             
        })
    .then((response)=>{ return response.json();}) 
    .then(result => {
        var data = result;
        statsSeasons(data)
         
    })
}

const statsSeasons = (data)=>{
    var res = data    

    if(res.player1.seasons.length >= res.player2.seasons.length){
        var season = res.player1.seasons 
    }else{
        var season = res.player2.seasons
    }   
    
    var player1 = String(res.player1.player).split(' ')
    if(player1.length == 1){ 
        player1 = player1[0]
    }else{
        player1 = player1[1]
    }

    var player2 = String(res.player2.player).split(' ')
    if(player2.length == 1){ 
        player2 = player2[0]
    }else{
        player2 = player2[1]
    }


    var glsSeasons = document.querySelector("#chart_glsSeasons").getContext('2d');

    gradient1 = glsSeasons.createLinearGradient(0, 0, 0, 450);
    gradient1.addColorStop(0, 'rgba(255, 0,0, 0.5)');
    gradient1.addColorStop(0.5, 'rgba(255, 0, 0, 0.25)');
    gradient1.addColorStop(1, 'rgba(255, 0, 0, 0)');



    
    const barData = {        
        labels : season,
        datasets: [
            {                
                label: player1 + "'s goals",
                data: res.player1.goals,                
                stack: 'Stack 0',
                fill: true,                 
                backgroundColor: gradient1,
                pointBackgroundColor: 'white',
                borderWidth: 1,
                borderColor: '#911215',
                
            },                       
            {
                label: player2 + "'s goals",
                data:  res.player2.goals,                
                stack: 'Stack 1',
                fill: 'start',  
                borderColor: '#cedddd',
                pointBackgroundColor: '#cedddd',
                borderWidth: 1,
            },              
        ]
    };   


    linechart1 = new Chart(glsSeasons,{  
        type: 'line',
        data: barData,
        options: {        
            
            interaction: {
                mode: 'index',
                intersect: true,
            },     
            plugins: {
                title: {
                    display: true,
                    text: "Player's Goals",
                    color:"#aaa",
                    textAlign: 'right'
                },
            },         
            // indexAxis: 'y',            
            responsive: true,
            scales: {
                x: {
                    stacked: true,
                },
                y: {
                    stacked: true
                }
            }
        }
    })


    const dataAssists = {        
        labels : season,
        datasets: [            
            {                
                label: player1 + "'s assists",
                data: res.player1.assists,
                backgroundColor: "red",
                stack: 'Stack 0',
                fill: 'start',  
                pointBackgroundColor: 'white',
            },            
            
            {                
                label: player2 + "'s assists",
                data: res.player2.assists,
                backgroundColor: "#aaad1",
                stack: 'Stack 1',
                fill: 'start',  
                pointBackgroundColor: 'white',                
            },    
            ]
    };

    var assSeasons = document.querySelector("#chart_assSeasons");


    linechart2 = new Chart(assSeasons,{  
        type: 'line',
        data: dataAssists,
        options: {        
            
            interaction: {
                mode: 'index',
                intersect: true,
            },     
            plugins: {
                title: {
                    display: true,
                    text: "Player's Assists",
                    color:"#aaa"
                },
            },         
            // indexAxis: 'y',            
            responsive: true,
            scales: {
                x: {
                    stacked: true,
                },
                y: {
                    stacked: true
                }
            }
        }
    })
}



const getStatsCompetition = (first_player,second_player)=>{
    fetch( `/player_comparison/bycompetition/${first_player}/${second_player}`,{ 
        headers:{
            'Content-Type':'application/json',                
            'X-CSRFToken' : getCookie('csrftoken')          
        },             
        })
    .then((response)=>{ return response.json();}) 
    .then(result => {
        var data = result;
        statsCompetition(data)      
        
    })
}

const statsCompetition = (data)=>{
    tableName = document.querySelectorAll(".table-players h1");
    tableName[0].innerHTML = data.player1.player;
    tableName[1].innerHTML = data.player2.player;


    var resTable =  document.querySelector('.res-table');

    for (i in data.player1.competition){    
        
        var performace = document.createElement("ul");
        performace.className = "performace";

        performace.innerHTML =  `
            <h1>${data.player1.competition[i]}</h1>
            <li class="table-data player1-games">${data.player1.games[i]}</li>
            <li class="table-data player1-assists">${data.player1.assists[i]}</li>
            <li class="table-data player1-goals" style="padding: 2vw 2vw 2vw 0;">${data.player1.goals[i]}</li>
            <li class="table-data player2-games">${data.player2.games[i]}</li>
            <li class="table-data player2-assists">${data.player2.assists[i]}</li>
            <li class="table-data player2-goals">${data.player2.goals[i]}</li>
        `
        resTable.appendChild(performace);


        if(data.player1.games[i] > data.player2.games[i]){
            document.querySelectorAll(".player1-games")[i].classList.add("red");
        }if(data.player1.games[i] < data.player2.games[i]){
            document.querySelectorAll(".player2-games")[i].classList.add("red");
        } 
    
        if(data.player1.goals[i] > data.player2.goals[i]){
            document.querySelectorAll(".player1-goals")[i].classList.add("red");
        }if(data.player1.goals[i] < data.player2.goals[i]){            
            document.querySelectorAll(".player2-goals")[i].classList.add("red");
        } 

        if(data.player1.assists[i] > data.player2.assists[i]){
            document.querySelectorAll(".player1-assists")[i].classList.add("red");
        }if(data.player1.assists[i] < data.player2.assists[i]){            
            document.querySelectorAll(".player2-assists")[i].classList.add("red");
        }     
    
    }      
}




    


