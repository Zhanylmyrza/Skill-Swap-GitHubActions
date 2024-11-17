const notify_socket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/chat/'
    +'notify/?token='
    + window.localStorage['access']
)

notify_socket.onopen = function(e){
    console.log("CONNECTED TO NOTIFICATION");
}

var count_badge = document.getElementById('count_badge')

notify_socket.onmessage = function(e){
    const data = JSON.parse(e.data)
    count_badge.innerHTML = data.count
    print("NOTIFY_SOCET.ONMESSAGE")
}

notify_socket.onclose = function(e){
    console.log("DISCONNECTED FROM NOTIFICATION");
}