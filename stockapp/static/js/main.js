  // const roomName = JSON.parse(document.getElementById('room-name').textContent);
  const socket = new WebSocket(
    'ws://' + window.location.host + '/ws/stock/' + '{{Stock|get_item:"symbol"}}/' + '{{room_name}}' + '/'
  );
// 
  socket.onmessage = function (e) {
    Data=JSON.parse(e.data) // get json object from backend (wesockets)
    var Cmp = document.getElementById('currentPrice')
    var changed = document.getElementById('change') 
    Cmp.innerHTML = Data['lastPrice'] // add CMP from json obj
       
    if ( Data['change'].toString().indexOf('-')===0) {
    changed.innerHTML = Data['change'] // add change in price from json obj 
    Cmp.classList.add('red');
    changed.classList.add('red');
    } else {
        Cmp.classList.add('green');
        changed.classList.add('green');
        changed.innerHTML = '+' + Data['change'] // add plus icon if increase
    }
    
  }
//   
  socket.onopen = function (e) {
    $.ajaxSetup({
      headers: { "X-CSRFToken": '{{csrf_token}}' }
    });
    $.ajax({
      type: 'POST',
      url: "http://127.0.0.1:8000/stock/{{Stock|get_item:'symbol'}}",
      data: {
        'data':
          '{{Stock|get_item:"symbol"}}',
      },
    });
  }
