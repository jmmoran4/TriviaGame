// const socket = io(wsProtocol + '://' + location.host,{transports: ["websocket"], secure: true});
//         socket.on("connect", function() {
//             socket.emit("my event", {data: "I\'m connected!"});
//         });


function startGame()
{
    //alert('Starting the sexy game...');
   // openPage('home.html');
    window.location.href = "/start"
}

function createUser()
{
    window.location.href = '/createUser'
}

// Need to use this as our entry point to connecting to websockets
function createLobby(username)
{
    // we want each players websocket url to be unique to them
        fetch('/create-lobby', {method: 'POST'})
        .then(response => response.json())
        .then(data => {
            window.location.href = 'lobby/${data.lobbyID}'
        })
        .catch(error => console.error('Failed to create lobby:', error))
}

/*
* Opens next page given a url address
* Example: openPage('page2.html')
*/ 
function openPage(url) 
{
    window.location.href = url;
}


function AskQuestion(category)
{
    const ZERO = 0;
    console.log(category);
    window.location.href = "/questionByType/" + category + "/" + ZERO.toString() + "/" + ZERO.toString();

}




