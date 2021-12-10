//Matt Hay ~ Web ~ 11/17/21

//called when the chat feed tab is selected

// add a listener so that when the document loads . . .
// new listeners can be attached to elements safely
var socket; 
document.addEventListener("DOMContentLoaded", function() {
	// make the initial connection to the webserver through the socket
    socket = io.connect('http://127.0.0.1:5000/game/');
    socket.on('connect', function() {
        console.log("Joined");
        socket.emit('joined', {});
    });

    //add an event listener for receiving messages from the server
    socket.on('message', function(data) {
        console.log("ARRIVED");
        let msgFeed = document.getElementById("msg-feed");

        //construct message div and its text
        var msgElement = document.createElement("div");
        msgElement.className = "left clearfix border-bottom my-1";
        var msgPara = document.createElement("p");
        msgPara.className = "mx-2";
        msgPara.textContent = `${data.msg}`;
        msgPara.style.color="MediumSeaGreen";
        msgPara.style.wordBreak="break-all";
        msgElement.appendChild(msgPara);
        msgFeed.appendChild(msgElement);
        msgFeed.scrollTop = msgFeed.scrollHeight;
    });

    //Get reference to chat tab button
    const openChatBtn = document.getElementById("openChat-btn");
    //add listener
    openChatBtn.addEventListener("click", openChatTab);

    //Get reference to character tab button
    const openCharEditBtn = document.getElementById("openCharEdit-btn");
    //add listener
    openCharEditBtn.addEventListener("click", openCharacterTab);

	// Get reference to send btn
	const sendMsgBtn = document.getElementById("sendMsg-btn");
	// Add event listener to the send btn
	sendMsgBtn.addEventListener("click", function(event) {
        let msgText = document.getElementById("msg-box");
        let username = document.getElementById("username");
        
        
        socket.emit('text', {msg: `${username.className}: ${msgText.value}`});
        msgText.value = "";
    });
    
    // Get reference to d6 btn
	const rollD6Btn = document.getElementById("roll-D6");
	// Add event listener to the d6 btn
	rollD6Btn.addEventListener("click", function(event) {
        let roll = Math.floor(Math.random() * 6);
        let username = document.getElementById("username");
        socket.emit('text', {msg: `${username.className} rolled a ${roll} with the D6 die`});
    });

    // Get reference to d10 btn
	const rollD10Btn = document.getElementById("roll-D10");
	// Add event listener to the d10 btn
	rollD10Btn.addEventListener("click", function(event) {
        let roll = Math.floor(Math.random() * 10);
        let username = document.getElementById("username");
        socket.emit('text', {msg: `${username.className} rolled a ${roll} with the D6 die`});
    });

    // Get reference to d20 btn
	const rollD20Btn = document.getElementById("roll-D20");
	// Add event listener to the d20 btn
	rollD20Btn.addEventListener("click", function(event) {
        let roll = Math.floor(Math.random() * 20);
        let username = document.getElementById("username");
        socket.emit('text', {msg: `${username.className} rolled a ${roll} with the D6 die`});
    });
});

//called when the live chat tab is selected 
function openChatTab()
{
    let chatTab = document.getElementById("livechat");
    let charEditTab = document.getElementById("characterEditor");

    chatTab.style.display = 'block';
    charEditTab.style.display = 'none';

    const openChatBtn = document.getElementById("openChat-btn");
    openChatBtn.style.backgroundColor = 'rgb(34, 105, 65)'
    const openCharEditBtn = document.getElementById("openCharEdit-btn");
    openCharEditBtn.style.backgroundColor = 'mediumseagreen'

}

//called when the character edit tab is selected 
function openCharacterTab()
{
    let chatTab = document.getElementById("livechat");
    let charEditTab = document.getElementById("characterEditor");

    console.log("HELLO");

    chatTab.style.display = 'none';
    charEditTab.style.display = 'block';

    const openChatBtn = document.getElementById("openChat-btn");
    openChatBtn.style.backgroundColor = 'mediumseagreen'
    const openCharEditBtn = document.getElementById("openCharEdit-btn");
    openCharEditBtn.style.backgroundColor = 'rgb(34, 105, 65)'
}