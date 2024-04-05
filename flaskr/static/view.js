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
    console.log(category)
    window.location.href = "/questionByType/" + category

}




