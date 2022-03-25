
const socket = new WebSocket(
    'ws://' + window.location.host + '/ws'+'/'+ 'Home' + '/'
    );
    socket.onmessage = function (e) {
    //   console.log(e.data)
        Data=JSON.parse(e.data) // get json object from backend (wesockets)
        console.log(Data.nifty50)
        console.log(Data)
        var Cmp = document.getElementById(Data.message['symbol'])
        var changed = document.getElementById(Data.message['symbol']+'change') 
        Cmp.innerHTML = '₹'+Data.message['lastPrice'] // add CMP from json obj
           
        console.log(Data.message['pChange'])
        if ( Data.message['pChange'].toString().indexOf('-')===0) {
        changed.innerHTML = Data.message['pChange']+'%' // add change in price from json obj 
        Cmp.classList.add('red');
        changed.classList.add('red');
        } 
        else {
            changed.innerHTML ='+' + Data.message['pChange']+'%'// add plus icon if increase
            Cmp.classList.add('green');
            changed.classList.add('green');
        }}
        // reload on page back 
        window.addEventListener( "pageshow", function ( event ) {
    var historyTraversal = event.persisted || 
                         ( typeof window.performance != "undefined" && 
                              window.performance.navigation.type === 2 );
    if ( historyTraversal ) {
    // Handle page restore.
    window.location.reload();
    }
    });
    // disable page forword
    $( document ).ready( function(){
    history.pushState(null,  document.title, location.href);        
    });
    
    