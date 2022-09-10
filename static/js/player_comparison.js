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
    var stats_ = document.querySelector('.general_stats')    

    stats_.innerHTML = `
        <table class="table">
        <thead>
            <tr>
                <th scope="col">Overall</th>
                <th scope="col" class="text-center">${player_1.player}</th>
                <th scope="col" class="text-end">${player_2.player}</th>                           
            </tr>
        </thead>
        <tbody class="table-group-divider">
            <tr>
                <th scope="row">Matches</th>
                <td class='text-center'>${player_1.Matches}</td>
                <td class="text-end">${player_2.Matches}</td>                
            </tr>
            <tr>
                <th scope="row">Goals</th>
                <td class='text-center'>${player_1.Goals}</td>
                <td class="text-end">${player_2.Goals}</td>                
            </tr> 
            <tr>
                <th scope="row">Ratio goals</th>
                <td class='text-center'>${player_1.Ratio_gls} %</td>
                <td class="text-end">${player_2.Ratio_gls} %</td>                
            </tr>    
            <tr>
                <th scope="row">Assists</th>
                <td class='text-center'>${player_1.Assists}</td>
                <td class="text-end">${player_2.Assists}</td>                
            </tr>               
            <tr>
                <th scope="row">Ratio assists</th>
                <td class='text-center'>${player_1.Ratio_ass} %</td>
                <td class="text-end">${player_2.Ratio_ass} %</td>                
            </tr>   
            <tr>
                <th scope="row">Goal involvements</th>
                <td class='text-center'>${player_1.rate_involvement} %</td>
                <td class="text-end">${player_2.rate_involvement} %</td>                
            </tr>                                   
        </tbody>                   
    ` 
    // document.querySelector('.page_loader').style.display  = 'none'
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
            <span class='title__competition'><h2>${e}</h2></span>
            <div class='stats'>
                <div class='player__'>                    
                    <div class='player__data'>
                        <span>${data.player_1.goals[i]}</span>
                        <label>GOALS</label>
                    </div> 
                    <div class='player__data'>
                        <span>${data.player_1.assists[i]}</span>
                        <label>ASSISTS</label>
                    </div>  
                    <div class='player__data'>
                        <span>${data.player_1.games[i]}</span>
                        <label>GAMES</label>
                    </div>                                     
                </div>
                <div class='player__'>
                    <div class='player__data'>
                        <span>${data.player_2.goals[i]}</span>
                        <label>GOALS</label>
                    </div> 
                    <div class='player__data'>
                        <span>${data.player_2.assists[i]}</span>
                        <label>ASSISTS</label>
                    </div>
                    <div class='player__data'>
                        <span>${data.player_2.games[i]}</span>
                        <label>GAMES</label>
                    </div>                    
                                           
                </div>
            </div>
        `

        // return [data.player_1.games[i],data.player_1.goals[i],data.player_1.assists[i], e, data.player_2.games[i],data.player_2.goals[i],data.player_2.assists[i]];
    });

   
    
    
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
  