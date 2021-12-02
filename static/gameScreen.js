//Matt Hay ~ Web ~ 11/17/21

//called when the chat feed tab is selected

// add a listener so that when the document loads . . .
// new listeners can be attached to elements safely
window.addEventListener("DOMContentLoaded", function() {
	
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
	sendMsgBtn.addEventListener("click", sendMessage);
    
    // Get reference to d6 btn
	const rollD6Btn = document.getElementById("roll-D6");
	// Add event listener to the d6 btn
	rollD6Btn.addEventListener("click", rollD6);

    // Get reference to d10 btn
	const rollD10Btn = document.getElementById("roll-D10");
	// Add event listener to the d10 btn
	rollD10Btn.addEventListener("click", rollD10);

    // Get reference to d20 btn
	const rollD20Btn = document.getElementById("roll-D20");
	// Add event listener to the d20 btn
	rollD20Btn.addEventListener("click", rollD20);
});


// Add message in message box to MSG feed
function sendMessage()
{
    let msgText = document.getElementById("msg-box");
    let username = document.getElementById("username");
    addMsgToFeed(`${username.className}: ${msgText.value}`);
    msgText.value = "";
}

//TODO: Add a name to the front of the message - custom "name" or default "server"
//create a div and add it to the feed
function addMsgToFeed(msg) 
{
    let msgFeed = document.getElementById("msg-feed");

    //construct message div and its text
    var msgElement = document.createElement("div");
    msgElement.className = "left clearfix border-bottom my-1";
    var msgPara = document.createElement("p");
    msgPara.className = "mx-2";
    msgPara.textContent = msg;
    msgPara.style.color="MediumSeaGreen";
    msgPara.style.wordBreak="break-all";
    msgElement.appendChild(msgPara);
    msgFeed.appendChild(msgElement);
    msgFeed.scrollTop = msgFeed.scrollHeight;

    //add msg to DB
}

//roll D6 die and add its output to MSG feed
function rollD6()
{
    let roll = Math.floor(Math.random() * 6);
    let username = document.getElementById("username");
    addMsgToFeed(`${username.className} rolled a ${roll} with the D6 die`);
}

//roll D10 die and add its output to MSG feed
function rollD10()
{
    let roll = Math.floor(Math.random() * 10);
    let username = document.getElementById("username");
    addMsgToFeed(`${username.className} rolled a ${roll} with the D10 die`);
}

//roll D20 die and add its output to MSG feed
function rollD20()
{
    let roll = Math.floor(Math.random() * 20);
    let username = document.getElementById("username");
    addMsgToFeed(`${username.className} rolled a ${roll} with the D20 die`);
}

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