// Let's Connect to our socket:
$(function () {
    // Correctly decide between ws:// and wss://
    var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    var ws_path = ws_scheme + '://' + window.location.host + "/chat/stream/";
    console.log("Connecting to "+ ws_path);
    var socket = new ReconnectingWebSocket(ws_path);


    // Helpful Debugging
    socket.onopen = function () {
        console.log("Connected to chat socket");
    };
    socket.onclose = function () {
        console.log("Disconnected From chat socket");
    };

    // Says if we joined a room or not by if there's a div for it.
    inRoom = function (roomId) {
        return $("#room-" + room.Id).length > 0;
    };

    // Room join/leave
    $('li.room-link').click(function () {
        roomId = $(this).attr("data-room-id");

        if (inRoom(roomId)) {
            // Leave Room
            $(this).removeClass("joined");
            socket.send(JSON.stringify({
                "command": "leave",     // determines which handler will be used (see chat/routing.py)
                "room": roomId
            }));

        } else {
            // Join room
            $(this).addClass("joined");
            socket.send(JSON.stringify({
                "command": "join",
                "room": roomId
            }));
        }

    });

    socket.onmessage = function (message) {

        // Decode the JSON
        console.log("Got websocket message" + message.data);
        var data = JSON.parse(message.data);
        // Handle Errors
        if (data.error) {
            alert(data.error);
            return;
        }

        // Handle Joining
        if (data.join) {
            console.log("Joining room" + data.join);
            var roomdiv = $(
                "<div class='room' id='room-" + data.join + "'>" +
                "<h2>" + data.title + "</h2>" +
                "<div class='messages'></div>" +
                "<input><button>Send</button>" +
                "</div>"
            );
            $("#chats").append(roomdiv);

            // Handle Leaving
        }  else if (data.leave) {
            console.log("Leaving room"+ data.leave);
            $("#room-" + data.leave).remove();
        } else {
            console.log("Cannot handle message!");
        }
    }

});