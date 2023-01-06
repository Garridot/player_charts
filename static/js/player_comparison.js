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

function get_players(first_player,second_player){
    // document.querySelector('.page_loader').style.display  = 'flex'
    get_general_stats(first_player,second_player) 
    get_goal_involvements(first_player,second_player)
    get_performance_competition(first_player,second_player)   
    get_goals_by_age(first_player,second_player)

    document.querySelector('#stats_1').style.display = 'none'
    document.querySelector('#stats_2').style.display = 'none'
    document.querySelector('.player_comparison').style.display = 'none'
}


function get_general_stats(first_player,second_player){ 
    var team = 'total' 
    fetch( `/general_stats/${first_player}/${team}` ,{ 
        headers:{
            'Content-Type':'application/json',                
            'X-CSRFToken' : getCookie('csrftoken')          
        },             
        })
    .then((response)=>{ return response.json();}) 
    .then(result => {
        var player_1 = result

        fetch( `/general_stats/${second_player}/${team}` ,{ 
            headers:{
                'Content-Type':'application/json',                
                'X-CSRFToken' : getCookie('csrftoken')          
            },             
            })
        .then((response)=>{ return response.json();}) 
        .then(result => {
            var player_2 = result
            render_general_stats(player_1,player_2)
        })     
            
    })  

    
}
function render_general_stats(player_1,player_2){


    document.querySelector('#stats_1').querySelector('.main_title').innerHTML = `<h1 style="font-size: 6rem;">${player_1.player}</h1>`

    var stats_ = document.querySelector('#stats_1').querySelector('.general')
    
    stats_.innerHTML = `
    <span>
        <h2>GOALS : ${player_1.Goals} </h2><h5>(${player_1.Ratio_gls} per game)</h5>     
    </span>
    <span>           
        <h2>ASSISTS : ${player_1.Assists}</h2> <h5>(${player_1.Ratio_ass} per game)</h5>    
    </span>         
    <span style='font-size: revert;'>
        <h2>INVOLVEMENTS PERCENTAGES:</h2>  <h2>${player_1.rate_involvement} %</h2>     
    </span>` ;

    document.querySelector('#stats_1').querySelector('.involvement').innerHTML = `
    <span>      
        <h2>${player_1.Matches} : MATCHES</h2> 
    </span>
    
    ` 

    document.querySelector('#stats_2').querySelector('.main_title').innerHTML = `<h1 style="font-size: 6rem;">${player_2.player}</h1>`

    var stats_2 = document.querySelector('#stats_2').querySelector('.general')
    
    stats_2.innerHTML = `
    <span>
        <h2>GOALS : ${player_2.Goals} </h2><h5>(${player_2.Ratio_gls} per game)</h5>     
    </span>
    <span>           
        <h2>ASSISTS : ${player_2.Assists}</h2> <h5>(${player_2.Ratio_ass} per game)</h5>    
    </span>         
    <span style='font-size: revert;'>
        <h2>INVOLVEMENTS PERCENTAGES:</h2>  <h2>${player_2.rate_involvement} %</h2>     
    </span>` ;

    document.querySelector('#stats_2').querySelector('.involvement').innerHTML = `
    <span>      
        <h2>${player_2.Matches} : MATCHES</h2> 
    </span>
    
    ` 
} 



function get_goal_involvements(first_player,second_player){     
    fetch( `/player_comparison/goal_involvements/${first_player}/${second_player}`,{ 
        headers:{
            'Content-Type':'application/json',                
            'X-CSRFToken' : getCookie('csrftoken')          
        },             
        })
    .then((response)=>{ return response.json();}) 
    .then(result => {
        var data = result
        render_goal_involvements(data)
    })
}
function render_goal_involvements(data){

    var ctx = document.querySelector('#involvements_chart').getContext('2d')   

    gradient = ctx.createLinearGradient(0, 0, 0, 450);
    gradient.addColorStop(0, 'rgba(255, 0,0, 0.1)');
    gradient.addColorStop(0.5, 'rgba(255, 0, 0, 0.1)');
    gradient.addColorStop(1, 'rgba(255, 0, 0, 0)');

    gradient2 = ctx.createLinearGradient(0, 0, 0, 450);
    gradient2.addColorStop(0, 'rgba(0, 77, 152, 0.5)');
    gradient2.addColorStop(0.5, 'rgba(0, 77, 152, 0.25)');
    gradient2.addColorStop(1, 'rgba(0, 77, 152, 0)');
    

    myLine = new Chart(ctx,{ 
        type:'line',
        data: {
            labels : data.seasons,
            datasets:[                            
                {
                    label : data.player1,
                    data  : data.goal_involvements_rate_player1,
                    fill: 'start',      
                              
                    backgroundColor: gradient,
                    borderColor: 'rgba(255, 0,0,0.5)', 
                    pointBackgroundColor: 'white',
                    borderWidth: 2,
                    tension: 0.1
                },
                {
                    label : data.player2,
                    data  : data.goal_involvements_rate_player2,
                    fill: 'start',
                    backgroundColor: gradient2,
                    borderColor: 'rgba(0, 77, 152,0.7)',
                    pointBackgroundColor: 'white',
                    borderWidth: 2,
                    tension: 0.1

                }            ]
        },
        options: {  
            maintainAspectRatio: false,              
            responsive: true,
                interaction: {
                mode: 'index',
                intersect: false,
            },
            scales: {
                y: {
                    ticks: { color: '#aaa', beginAtZero: true }
                },
                x: {
                    ticks: { color: '#aaa', beginAtZero: true }
                }
            },
            plugins: {
                title: {
                    display: true,
                    text: 'Goal Involvements by Season.',
                    font: {
                        fontSize: 50
                    },
                    padding: {
                        top: 10,
                        bottom: 30
                    },
                    color: "#aaa"
                },
                legend: {
                    display:true,
                    labels: {
                        color: '#aaa',                            
                    }
                },
                
            }
        }           
        
    })
}



function get_performance_competition(first_player,second_player){
    fetch( `/player_comparison/performance_competition_players/${first_player}/${second_player}`,{ 
        headers:{
            'Content-Type':'application/json',                
            'X-CSRFToken' : getCookie('csrftoken')          
        },             
        })
    .then((response)=>{ return response.json();}) 
    .then(result => {
        var data = result
        render_performance_competition(data)        
    })
}
function render_performance_competition(data){
    var table = document.querySelector('.competitions')
    

    data.player_1.competitions.map(function(e, i) {
        

        table.innerHTML += 
        `

        <div class="section__competitions" >
            <span class='title__competition'><h2>${e}</h2></span> 
            <div class="stats">
                <div class='player__'>
                    <span class="player__name"><h4>${data.player_1.name}</h4></span>
                    <div class='player__data'>
                        <div class="boxes">
                            <span>
                                <h3>${data.player_1.games[i]}</h3>
                                <label>APPS</label>
                            </span>
                            <span>
                                <h3>${data.player_1.assists[i]}</h3>
                                <label>ASSISTS</label>
                            </span>
                            <span>
                                <h3>${data.player_1.goals[i]}</h3>
                                <label>GOALS</label>
                            </span>
                        </div>   
                                    
                    </div>  
                </div>
                <div class='player__2'>
                    <span class="player2__name"><h4>${data.player_2.name}</h4></span>
                    <div class='player2__data'>
                        <div class="boxes">
                            <span>
                                <h3>${data.player_2.goals[i]}</h3>
                                <label>GOALS</label>
                            </span>
                            <span>
                                <h3>${data.player_2.assists[i]}</h3>
                                <label>ASSISTS</label>
                            </span>
                            <span>
                                <h3>${data.player_2.games[i]}</h3>
                                <label>APPS</label>
                            </span>
                        </div>
                                        
                    </div>  
                </div>    
            </div>
        </div>            
        `        
    });
    
    document.querySelector('#stats_1').style.display = 'block'
    document.querySelector('#stats_2').style.display = 'block'
    document.querySelector('.player_comparison').style.display = 'block'
    document.querySelector('.page_loader').style.display  = 'none'
}


function get_goals_by_age(first_player,second_player){     
    fetch( `/player_comparison/goals_by_age/${first_player}/${second_player}`,{ 
        headers:{
            'Content-Type':'application/json',                
            'X-CSRFToken' : getCookie('csrftoken')          
        },             
        })
    .then((response)=>{ return response.json();}) 
    .then(result => {
        var data = result
        render_goals_by_age(data)
    })
}

function render_goals_by_age(data){
    var ctx = document.querySelector('#by_age').getContext('2d')     
    gradient = ctx.createLinearGradient(0, 0, 0, 450);
    gradient.addColorStop(0, 'rgba(255, 0,0, 0.1)');
    gradient.addColorStop(0.5, 'rgba(255, 0, 0, 0)');
    gradient.addColorStop(1, 'rgba(255, 0, 0, 0)');
    myLine = new Chart(ctx,{ 
        type:'line',
        data: {
            labels : data.ages,
            datasets:[                            
                {
                    label : data.p1,
                    data  : data.goals_p1,
                    fill: 'start',       
                    backgroundColor: gradient,             
                    borderColor: 'rgba(255, 0,0,0.5)', 
                    pointBackgroundColor: 'white',
                    borderWidth: 2.5,
                    tension: 0.2
                },
                {
                    label : data.p2,
                    data  : data.goals_p2,
                    fill: 'start',
                    borderColor: 'rgba(237, 187, 0,0.5)',
                    pointBackgroundColor: 'white',
                    borderWidth: 2.5,
                    tension: 0.2
                }            ]
        },
        options: {  
            maintainAspectRatio: false,              
            responsive: true,
                interaction: {
                mode: 'index',
                intersect: false,
            },
            scales: {
                y: {
                    ticks: { color: '#aaa', beginAtZero: true }
                },
                x: {
                    ticks: { color: '#aaa', beginAtZero: true }
                }
            },
            plugins: {
                title: {
                    display: true,
                    text: 'Goals Evolution by Ages.',
                    font: {
                        fontSize: 50
                    },
                    padding: {
                        top: 10,
                        bottom: 30
                    },
                    color: "#aaa"
                },
                legend: {
                    display:true,
                    labels: {
                        color: '#aaa',                            
                    }
                },
                
            }
        }           
        
    })
}
  