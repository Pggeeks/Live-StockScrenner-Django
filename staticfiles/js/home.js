
const socket = new WebSocket(
    'ws://' + window.location.host + '/ws'+'/'+ 'Home' + '/'
    );
    socket.onmessage = function (e) {
        Data=JSON.parse(e.data) // get json object from backend (wesockets)
        // updating nifty50 and nifty bank
        // console.log(Data.niftyBank.lastPrice)
        var N50 = document.getElementById(Data.nifty50.name)
        // N50.innerHTML = '₹'+Data.nifty50.lastPrice
        var chng = document.getElementById(Data.nifty50.name+'change')
        var chngb = document.getElementById(Data.niftyBank.name+'change')
        chng.innerHTML = Data.nifty50.pChange + '%'
        var NBNK = document.getElementById(Data.niftyBank.name)
        document.getElementById(Data.niftyBank.name+'change').innerHTML =Data.niftyBank.pChange +'%'
        if ( Data.nifty50.pChange.toString().indexOf('-')===0) {
            chng.innerHTML = Data.nifty50.pChange+'%' // add change in price from json obj 
            N50.classList.add('red');
            chng.classList.add('red');
            // changed.classList.add('red');
            } 
            else {
                chng.innerHTML ='+' + Data.nifty50.pChange+'%'// add plus icon if increase
                N50.classList.add('green');
                chng.classList.add('green');
            }
        if ( Data.niftyBank.pChange.toString().indexOf('-')===0) {
            chng.innerHTML = Data.niftyBank.pChange+'%' // add change in price from json obj 
            NBNK.classList.add('red');
            chngb.classList.add('red');
            // changed.classList.add('red');
            } 
            else {
                chngb.innerHTML ='+' + Data.niftyBank.pChange+'%'// add plus icon if increase
                NBNK.classList.add('green');
                chngb.classList.add('green');
            }
        //  other stocks top list
        console.log(Data.message['symbol'])
        var Cmp = document.getElementById(Data.message['symbol'])
        var changed = document.getElementById(Data.message['symbol']+'change') 
        Cmp.innerHTML = '₹'+Data.message['lastPrice'] // add CMP from json obj
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


    $.ajax(
        {
        type:"GET",
        url: "ajax/get-info",
        success: function(data) 
        {
            // console.log(data)
            AvailableTags=Object.keys(data);
            console.log(AvailableTags)
            $("#tags").autocomplete({
                source: AvailableTags,
                selectFirst: true,
                minLength: 2,
                open: function () {
                    setTimeout(function () {
                        $('.ui-autocomplete').css('z-index', 1000000);
                        // 
                        // 
                    });
                    $(".ui-autocomplete li").click(function () {
                        var name = ($(this).text()); // gets text contents of clicked li    
                        window.location.href = `stock/${name}`
                    });

                }

            });
        }
});
// adding nifty 50 and nifty bank using ajax request //
$.ajax({
    type:"GET",
        url: "ajax/get-nifty",
        success: function(e) 
        {
            console.log(e.nifty50.name)
            document.getElementById("nifty-cards").innerHTML +=`
            <div id="nifty-items" class="card border border-success mb-3">
                <div class="card-body text-primary">
                    <h5 class="card-title text-dark">${e.nifty50.name}</h5>
                    <p class="card-text" id="${e.nifty50.name}">₹${e.nifty50.lastPrice}</p>
                    <p id="${e.nifty50.name}change" class="card-text m-0">${e.nifty50.pChange}%</p>
                    </div>
                `;
                document.getElementById("nifty-cards").innerHTML +=`
            <div id="nifty-items" class="card border border-success mb-3">
                <div class="card-body text-primary" id="">
                    <h5 class="card-title text-dark">${e.niftyBank.name}</h5>
                    <p class="card-text" id="${e.niftyBank.name}">₹${e.niftyBank.lastPrice}</p>
                    <p id="${e.niftyBank.name}change" class="card-text m-0">${e.niftyBank.pChange}%</p>
                    </div>
                `;
        }
});
    $.ajax({
        type:"GET",
        url: "ajax/get-topstocks",
        success: function(e) 
        {
            // making html through ajax updating inputs through websockets
            for (var i=0; i < Object.keys(e).length; i++) {

                if ( e[i].pChange.toString().indexOf('-')===0) {
                    document.getElementById('stocklistmain').innerHTML +=`
                    <tr _ngcontent-nuh-c18="" id="stocklist">
                    <td _ngcontent-nuh-c18=""><i _ngcontent-nuh-c18=""
                                                            class="icon ion-md-star"></i> <a style="color: black;" href="stock\\${e[i].symbol}">${e[i].symbol}</a></td>
                                                    <td _ngcontent-nuh-c18="" id="${e[i].symbol}"" class="red">
                                                        ₹${e[i].lastPrice}</td>
                                                    <td _ngcontent-nuh-c18="" id="${e[i].symbol}change"
                                                        class='red'>${e[i].pChange}%</td>
                                                   
                                                    <td _ngcontent-nuh-c18="">${e[i].dayHigh}</td>
                                                    <td _ngcontent-nuh-c18="">${e[i].dayLow}</td>
                                                    <td _ngcontent-nuh-c18="">${e[i].totalTradedVolume}</td>
                                                </tr>
                                                `
                }
                else{
                    document.getElementById('stocklistmain').innerHTML +=`
                    <tr _ngcontent-nuh-c18="" id="stocklist">
                    <td _ngcontent-nuh-c18=""><i _ngcontent-nuh-c18=""
                                                            class="icon ion-md-star"></i> <a style="color: black;" href="stock\\${e[i].symbol}">${e[i].symbol}</a></td>
                                                    <td _ngcontent-nuh-c18="" id="${e[i].symbol}"" class="green">
                                                        ₹${e[i].lastPrice}</td>
                                                    <td _ngcontent-nuh-c18="" id="${e[i].symbol}change"
                                                        class='green'>+${e[i].pChange}%</td>
                                                    <td _ngcontent-nuh-c18="">${e[i].dayHigh}</td>
                                                    <td _ngcontent-nuh-c18="">${e[i].dayLow}</td>
                                                    <td _ngcontent-nuh-c18="">${e[i].totalTradedVolume}</td>
                                                </tr>
                                                `
                }
        }}
    });
    
    