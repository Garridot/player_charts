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

function get_path(path){
    var select = document.querySelector('.filters');
    var team = select.options[select.selectedIndex].value  

    get_general_stats(path,team);
    get_gls_as_season(path,team);
    get_goal_involvements(path,team); 
    get_performance_competition(path,team); 
}

function get_general_stats(path,team){   
    fetch( `/general_stats${path}/${team}` ,{                            
            method:'POST',
            headers:{
                'Content-Type':'application/json',                
                'X-CSRFToken' : getCookie('csrftoken')          
            }, 
        })
    .then((response)=>{ return response.json();}) 
    .then(result => {
        var data = result
        render_stats(data);
        
    })         
}
function render_stats(data){    

    var stats_ = document.querySelector('.general')    

    stats_.innerHTML = `
    <span>
        <h2>GOALS : ${data.Goals} </h2><h5>(${data.Ratio_gls} per game)</h5>     
    </span>
    <span>           
        <h2>ASSISTS : ${data.Assists}</h2> <h5>(${data.Ratio_ass} per game)</h5>    
    </span>         
    <span style='font-size: revert;'>
        <h2>INVOLVEMENTS PERCENTAGES:</h2>  <h2>${data.rate_involvement} %</h2>     
    </span>` ;

    document.querySelector('.involvement').innerHTML = `
    <span>      
        <h2>${data.Matches} : MATCHES</h2> 
    </span>
    
    ` 
}


function get_gls_as_season(path,team){
    fetch( `/gls_as_season${path}/${team}` ,{                            
            method:'POST',
            headers:{
                'Content-Type':'application/json',                
                'X-CSRFToken' : getCookie('csrftoken')          
            }, 
        })
    .then((response)=>{ return response.json();}) 
    .then(result => {
        var   res = result
        
        render_gls_as_season(res)
    })
}
let myLine;
function render_gls_as_season(res){

    var ctx = document.querySelector('#gls_as_season').getContext('2d')
    if (myLine) {
        myLine.destroy();
    }

    if(res.Seasons.length >= 2){
        document.querySelector('.section_gls_as_season').style.display = 'block'
        
        gradient = ctx.createLinearGradient(0, 0, 0, 450);
        gradient.addColorStop(0, 'rgba(255, 0,0, 0.1)');
        gradient.addColorStop(0.5, 'rgba(255, 0, 0, 0.1)');
        gradient.addColorStop(1, 'rgba(255, 0, 0, 0)');

        gradient2 = ctx.createLinearGradient(0, 0, 0, 450);
        gradient2.addColorStop(0, 'rgba(0, 77, 152, 0.5)');
        gradient2.addColorStop(0.5, 'rgba(0, 77, 152, 0.25)');
        gradient2.addColorStop(1, 'rgba(0, 77, 152, 0)');

        gradient3 = ctx.createLinearGradient(0, 0, 0, 450);
        gradient3.addColorStop(0, 'rgba(168, 19, 62, 0.5)');
        gradient3.addColorStop(0.75, 'rgba(168, 19, 62, 0.4)');
        gradient3.addColorStop(0.5, 'rgba(168, 19, 62, 0.3)');
        gradient3.addColorStop(0.25, 'rgba(168, 19, 62, 0.2)');
        gradient3.addColorStop(1, 'rgba(168, 19, 62, 0.25)');
    
        myLine = new Chart(ctx,{                              
                
            type:'line',
            data: {
                labels : res.Seasons,
                datasets:[            
                    {
                        label : 'Goals',
                        data  : res.Goals,
                        fill: 'start',                   
                        backgroundColor: gradient,
                        borderColor: '#911215', 
                        pointBackgroundColor: 'white',
                        borderWidth: 1,
                        tension: 0.1
                    },
                    {
                        label : 'Assists',
                        data  : res.Assists,
                        fill: 'start',
                        backgroundColor: gradient2,
                        borderColor: '#004D98',
                        pointBackgroundColor: 'white',
                        borderWidth: 1,
                        tension: 0.2
                    },                
                    {
                        label : 'Goals involvements',
                        data: res.Player_part,
                        fill: 'start',                    
                        borderColor: 'rgba(237, 187, 0)',
                        pointBackgroundColor: 'white',
                        borderWidth: 1,
                        tension: 0.2
                    },
                    {
                        label : "Team's Goals",
                        data: res.Team_gls,
                        fill: 'start',
                        backgroundColor: gradient3,
                        // borderColor: '#004D98',
                        pointBackgroundColor: 'white',
                        borderWidth: .5,
                        tension: 0.2,
                        type: 'bar',
                    },       
            ]
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
                        text: 'Goals & Assists In Each Season.',
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
    }else{
        document.querySelector('.section_gls_as_season').style.display = 'none'
    } 
}


function get_goal_involvements(path,team){
    fetch( `/goal_involvements${path}/${team}` ,{                            
            method:'POST',
            headers:{
                'Content-Type':'application/json',                
                'X-CSRFToken' : getCookie('csrftoken')          
            }, 
        })
    .then((response)=>{ return response.json();}) 
    .then(result => {
        var   res = result
        render_goal_involvements(res)
        
        
    })
}

let myBar;
function render_goal_involvements(res){
        
    var ctx2 = document.querySelector('#involvements').getContext('2d') 

    if (myBar) {
        myBar.destroy();
    }
    if(res.Seasons.length >= 2){

        document.querySelector('.section_involvements').style.display = 'block'
        gradient = ctx2.createLinearGradient(0, 0, 0, 450);
        gradient.addColorStop(0, 'rgba(237, 187,0)');
        gradient.addColorStop(0.75, 'rgba(237, 187,0, 0.75)');
        gradient.addColorStop(0.5, 'rgba(237, 187,0, 0.5)');
        gradient.addColorStop(0.25, 'rgba(237, 187,0, 0.25)');

        myBar = new Chart(ctx2,{ 
            type: 'bar',
            data: {
                labels : res.Seasons,
                datasets:[{
                    data  : res.involvements,
                    label : 'Goals Involvements Percentages', 
                    backgroundColor:gradient,                                     
                }               
            ]},
            options: {                
                // indexAxis: 'y', 
                maintainAspectRatio: false,                   
                elements: {
                    bar: {
                    borderWidth: 2,
                    }
                },
                scales: {
                    y: {
                        ticks: { color: '#aaa', beginAtZero: true }
                    },
                    x: {
                        ticks: { color: '#aaa', beginAtZero: true }
                    }
                },            
                responsive: true,
                plugins: {
                    legend: {
                    display:true,
                    labels: {
                        color: '#aaa'
                    }
                },
                title: {
                    display: true,
                    text: "Goal Involvements In Each Season.",
                    padding: {
                        top: 10,
                        bottom: 30
                    },
                    color: "#aaa"
                }
            }}
        })
    }else{
        document.querySelector('.section_involvements').style.display = 'none'
    }
    
}


function get_performance_competition(path,team){
    fetch( `/performance_competition${path}/${team}` ,{                            
        method:'POST',
        headers:{
            'Content-Type':'application/json',                
            'X-CSRFToken' : getCookie('csrftoken')          
        }, 
    })
    .then((response)=>{ return response.json();}) 
    .then(result => {
        var res = result       
        render_table(res)
            
    })
}

function render_table(res){

    let tbody =  document.querySelector('.tbody')
    var table =  document.querySelector('.table')

    
        
    while (tbody.hasChildNodes()){                
        tbody.removeChild(tbody.lastChild);}
 
    
    for (i in res.Competition){
        tbody.innerHTML += `
        <tr>
            <th scope="col">${res.Competition[i]}</th>
            <th scope="col">${res.games[i]}</th>
            <th scope="col">${res.goals[i]}</th>
            <th scope="col">${res.assists[i]}</th>
            <th scope="col">${res.performance[i]}%</th>
        </tr>
        `
       
    }
    // table.innerHTML = tbody

    // var c = a.map(function(e, i) {
    //     return [e, b[i]];
    //   });
    

    
    
}

