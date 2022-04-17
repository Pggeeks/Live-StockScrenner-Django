if (performance.navigation.type == 2) {
  location.reload(true);
  // reload page
}
//  getting stockname from django template
var Data_From_Template = JSON.parse(document.getElementById('StockName').textContent);
const socket = new WebSocket(
  'wss://' + window.location.host + '/ws/stock/' + Data_From_Template + '/'
);
socket.onmessage = function (e) {
  // directly setting inputs through web sockets
  Data = JSON.parse(e.data) // get json object from backend (wesockets)
  console.log(Data['lastPrice'])
  var Cmp = document.getElementById('currentPrice')
  var changed = document.getElementById('change')
  Cmp.innerHTML = '₹' + Data['lastPrice'] // add CMP from json obj

  if (Data['pChange'].toString().indexOf('-') === 0) {
    changed.innerHTML = Data['pChange'] + '%' // add change in price from json obj 
    Cmp.classList.add('red');
    changed.classList.add('red');
  } else {
    Cmp.classList.add('green');
    changed.classList.add('green');
    changed.innerHTML = '+' + Data['pChange'] + '%' // add plus icon if increase
  }

}

function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie != '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
      var cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) == (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
var spinner = `
<div id='loading'>
<div class="spinner-border" role="status">
<div class="sr-only">Loading...</div>
</div>
</div>`
$(document).ready(function () {
  $.ajax({
    type: "POST",
    url: "ajax/Get-SelectedStock/",
    data: {
      csrfmiddlewaretoken: getCookie('csrftoken'),
      Name: Data_From_Template,
    },
    success: function (e) {
      document.getElementById('Company_Des').innerHTML += e
    },
    beforeSend: function () {
      $('.load').html(spinner);
    },
    complete: function () {
      $('#loading').remove();
    },
  })
});
