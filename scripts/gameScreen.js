// add a listener so that when the document loads . . .
// new listeners can be attached to elements safely
window.addEventListener("DOMContentLoaded", function() {
	
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
    let msgText = document.getElementById("msg-box").textContent;
    addMsgToFeed(msg);
}

//create a div and add it to the feed
function addMsgToFeed(msg) 
{
    let msgFeed = document.getElementById("msg-feed");

    var msgElement = document.createElement("div");
    msgElement.class = "left clearfix border-bottom my-1";
    var para = document.createElement("p");
    para.textContent = msg;
    para.style.color="MediumSeaGreen";
    msgElement.appendChild(para);
    msgFeed.appendChild(msgElement);

    //add msg to DB
}

//roll D6 die and add its output to MSG feed
function rollD6()
{
    let roll = Math.floor(Math.random() * 6);
    addMsgToFeed(`User rolled a ${roll} with the D6 die`);
}

//roll D10 die and add its output to MSG feed
function rollD10()
{
    let roll = Math.floor(Math.random() * 10);
    addMsgToFeed(`User rolled a ${roll} with the D10 die`);
}

//roll D20 die and add its output to MSG feed
function rollD20()
{
    let roll = Math.floor(Math.random() * 20);
    addMsgToFeed(`User rolled a ${roll} with the D20 die`);
}