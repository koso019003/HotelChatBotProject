//- Using a function pointer:
document.getElementById("record").onclick = record;
//document.getElementById("search").onclick = search;
document.getElementById("signature_block").onclick = show_sign;

const GUEST_PHOTO = [
  "/static/base/image/girl.png",
  "/static/base/image/boy.png",
];
const GUEST_VIDEO = [
  "/static/base/video/female.mp4",
  "/static/base/video/male.mp4",
];

const msgerForm = get(".msger-inputarea");
const msgerInput = get(".msger-input");
const msgerChat = get(".msger-chat");
const folioForm = get("#document");
const myVideo = get("#guest_video");
const BOT_MSGS = [
  "Sorry, something wrong. I should leave now",
  "Bye",
  "See you",
  "Bug is coming",
  "Fix my bug now"
];

// Icons made by Freepik from www.flaticon.com
const BOT_IMG = "/static/base/image/msg_robot.svg";
const PERSON_IMG = "/static/base/image/msg_boy.svg";
//const BOT_IMG = "https://image.flaticon.com/icons/svg/327/327779.svg";
//const PERSON_IMG = "https://image.flaticon.com/icons/svg/145/145867.svg";
const BOT_NAME = "GUEST";
const PERSON_NAME = "FOA";
const USER_ID = "koso_web";

var INPUT_HISTORY = [];
var INPUT_HISTORY_INDEX = -1;

$(document).ready(function(){
  $(".msger-input").keydown(function(e){
    if (e.keyCode == '38') {
        // up arrow
        if (INPUT_HISTORY_INDEX < INPUT_HISTORY.length - 1){
            INPUT_HISTORY_INDEX = INPUT_HISTORY_INDEX + 1;
        }
        if (INPUT_HISTORY_INDEX == INPUT_HISTORY.length || INPUT_HISTORY_INDEX == -1){
            msgerInput.value = '';
        }
        else {
            msgerInput.value = INPUT_HISTORY[INPUT_HISTORY_INDEX];
        }
    }
    else if (e.keyCode == '40') {
        // down arrow
        if (INPUT_HISTORY_INDEX > -1){
            INPUT_HISTORY_INDEX = INPUT_HISTORY_INDEX - 1;
        }
        if (INPUT_HISTORY_INDEX == -1){
            msgerInput.value = '';
        }
        else {
            msgerInput.value = INPUT_HISTORY[INPUT_HISTORY_INDEX];
        }
    }
  });

  ready();
  $('#guest_photo').show();
});


msgerForm.addEventListener("submit", event => {
  event.preventDefault();
  if (myVideo.paused) myVideo.play();
  const msgText = msgerInput.value;

  if (!msgText) return;

  appendMessage(PERSON_NAME, PERSON_IMG, "right", msgText);
  msgerInput.value = "";

  if (msgText == '/reset'){
    appendMessage(BOT_NAME, BOT_IMG, "left", 'Resetting...');
    setTimeout(reset, 800);
  }else{
    botResponse(msgText);
  }

  INPUT_HISTORY.unshift(msgText);
  if (INPUT_HISTORY.length > 20){
    INPUT_HISTORY = INPUT_HISTORY.slice(0, 20)
  }
  INPUT_HISTORY_INDEX = -1;
});

folioForm.addEventListener("submit", event => {
  event.preventDefault();
  $('.reg_field').attr('readonly', true);
  $.ajax({
        url: 'submit_bill/',
        type: 'post',
        data: $('#document').serialize(),
        success: function(){
            alert("Submit!");
        },
        error: function(){
            alert("Fail!");
        },
    });
});

var recording = false;

if (!('webkitSpeechRecognition' in window)) {
  alert("This browser don't provid SpeechRecognition! Please use chrome.");
} else {
  console.log('webkitSpeechRecognition available.');
  var recognition = new webkitSpeechRecognition();

  recognition.continuous=false;
  recognition.interimResults=false;
  recognition.lang="en-US";

  recognition.onstart=function(){
    var record_btn = get("#record");

    console.log('開始辨識...');
    record_btn.style.color = "red";
    record_btn.innerHTML = "Stop";
  };
  recognition.onend=function(){
    var record_btn = get("#record");

    console.log('停止辨識!');
    record_btn.style.color = "#fff";
    record_btn.innerHTML = "Record";
  };

  recognition.onresult=function(event){
    console.log(event);
    var i = event.resultIndex;
    var j = event.results[i].length-1;
    msgerInput.value = msgerInput.value + event.results[i][j].transcript;
  };
}

function record() {
  if (!recording){
      // alert("This browser provid SpeechRecognition!");
      recording = true;
      recognition.start();
    }
  else{
      recognition.stop();
      recording = false;
  }
}

function ready(){
    const x = random(0, 2);
//    console.log(x);
    $('#guest_photo').attr('src',GUEST_PHOTO[x]);
    var source = document.createElement('source');
    source.setAttribute('src', GUEST_VIDEO[x]);
    myVideo.appendChild(source);
    $.get("ready/", {'gender':x});
}

function show_sign() {
    $.get("reg_show_sign/");
    document.getElementById("signature_block").style.borderColor  = "red";
}

function appendMessage(name, img, side, text) {
  //   Simple solution for small apps

  const msgHTML = `
    <div class="msg ${side}-msg">
      <div class="msg-img" style="background-image: url(${img})"></div>

      <div class="msg-bubble">
        <div class="msg-info">
          <div class="msg-info-name">${name}</div>
          <div class="msg-info-time">${formatDate(new Date())}</div>
        </div>

        <div class="msg-text">${text}</div>
      </div>
    </div>
  `;
  msgerChat.insertAdjacentHTML("beforeend", msgHTML);
  msgerChat.scrollTop += 500;
}

function appendCard(name, img, side, title, context) {
  //   Simple solution for small apps

  const msgHTML = `
    <div class="msg ${side}-msg">
      <div class="msg-img" style="background-image: url(${img})"></div>

      <div class="msg-bubble">
        <div class="msg-info">
          <div class="msg-info-name">${name}</div>
          <div class="msg-info-time">${formatDate(new Date())}</div>
        </div>

        <div class="card">
            <div class="card-container">
                <h4><b>${title}</b></h4>
                <p>${context}</p>
                <p>...</p>
            </div>
        </div>
      </div>
    </div>
  `;
  msgerChat.insertAdjacentHTML("beforeend", msgHTML);
  msgerChat.scrollTop += 500;
}

function botResponse(message) {

  $.ajax({
        url: "chat",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({ message: message, sender: USER_ID}),
        success: function(response, status) {
            console.log("Response from Webhook: ", response, "\nStatus: ", status);

//            // if user wants to restart the chat and clear the existing chat contents
//            if (message.toLowerCase() == '/restart') {
//                $("#userInput").prop('disabled', false);
//
//                //if you want the bot to start the conversation after restart
//                // action_trigger();
//                return;
//            }
            appendMessage(BOT_NAME, BOT_IMG, "left", response["response"]);

            if (response['action']){
                if (response['action'] == 'show_card'){
                    appendCard(
                    BOT_NAME, BOT_IMG, "left",
                    response['params']['title'], response['params']['content'])
                }
                if (response['action'] == 'finalize'){
                    alert(response['params'])
                    setTimeout(reset, 1000);
                }
                if (response['action'] == 'fill_signature'){
                    folioForm.elements["signature"].value = response['params']['signature'];
                }
                if (response['action'] == 'complete'){
                    botResponse('/complete');
                }
            }

        },
        error: function(xhr, textStatus, errorThrown) {
            // if there is no response from rasa server
            const r = random(0, BOT_MSGS.length - 1);
            const msgText = BOT_MSGS[r];

            appendMessage(BOT_NAME, BOT_IMG, "left", msgText);
            console.log("Error from Webhook: ", textStatus);
            setTimeout(reset, 1000);
        }
    });
}

// Utils
function get(selector, root = document) {
  return root.querySelector(selector);
}

function formatDate(date) {
  const h = "0" + date.getHours();
  const m = "0" + date.getMinutes();

  return `${h.slice(-2)}:${m.slice(-2)}`;
}

function random(min, max) {
  return Math.floor(Math.random() * (max - min) + min);
}

function reset() {
    msgerChat.innerHTML = `
    <div class="msg left-msg">
        <div
                class="msg-img"
                style="background-image: url(${BOT_IMG})"
        ></div>

        <div class="msg-bubble">
            <div class="msg-info">
                <div class="msg-info-name">BOT</div>
                <div class="msg-info-time">12:45</div>
            </div>

            <div class="msg-text">
                Hi, I am your practice partner.<br>From now on, I play your guest.😄
                <br><br><b>Comment:</b><br>
                1. /reset: to restart a new dialogue<br>
                2. /complete: to finalize current dialogue and calculate your score
            </div>
        </div>
    </div>
  `;

    document.getElementById("output").innerHTML = "";
    folioForm.reset();
    get("#search-panel").elements["last_name"].value = "";
    get("#search-panel").elements["room_num"].value = "";

    $('.reg_field').attr('readonly', false);
    document.getElementById("result").innerHTML = "";
    document.getElementById("signature_block").style.borderColor  = "";

    for (var i=1; i<10; i++){
        document.getElementById("add_qty"+i).style.display = "none";
    }
    ready();
}

function search() {

    var last_name = $("#last_name").val();
    var room_num = $("#room_num").val();

    $.get("search/",{'last_name':last_name,'room_num':room_num}, function(ret){
        //$('#result').html(ret["result"])
        console.info(ret)
        if (ret["result"] == "Find!"){
            folioForm.elements["g_name"].value = ret['full_name']
            folioForm.elements["folio_no"].value = ret['folio_no']
            folioForm.elements["room_no"].value = ret['room_num']
            folioForm.elements["a_date"].value = ret['a_date']
            folioForm.elements["d_date"].value = ret['d_date']
            folioForm.elements["a_c_no"].value = ret['a_c_num']
            folioForm.elements["cashier_id"].value = ret['cashier_id']
            folioForm.elements["page"].value = ret['page']
            folioForm.elements["p_date"].value = ret['print_date']
            var num = 1;
            var totalGST = 0;
            var GST = 0;
            var b_date = ret['a_date'];
            for(var i=1; i<parseInt(ret['duration'])+1;i++){
                folioForm.elements['b_date' + num].value = b_date;
                folioForm.elements['b_desc' + num].value='Accommodation Charge';
                num += 1;
                folioForm.elements['b_date' + num].value = b_date;
                folioForm.elements['b_desc' + num].value='Accommodation - Service Charge';
                num += 1;
                folioForm.elements['b_date' + num].value = b_date;
                folioForm.elements['b_desc' + num].value='Accommodation Charge - GST';
                num += 1;
                folioForm.elements['ac' + i].value = parseFloat(ret['r_rate']).toFixed(2);
                folioForm.elements['sc' + i].value = (parseFloat(ret['r_rate']) * 0.1).toFixed(2);
                GST += parseFloat(ret['r_rate']) * 0.07;
                folioForm.elements['GST' + i].value = (parseFloat(ret['r_rate'])*0.07).toFixed(2);
                totalGST += parseFloat(ret['r_rate']) + parseFloat(ret['r_rate'])*0.1 + parseFloat(ret['r_rate'])*0.07;
                b_date = ret['stay_'+(i+1)+'_date'];
            }

            folioForm.elements['total'].value = totalGST.toFixed(2);
            folioForm.elements['bal_due'].value = totalGST.toFixed(2);
            folioForm.elements['total_no_GST'].value = (totalGST - GST).toFixed(2);
            folioForm.elements['GST'].value = GST.toFixed(2);
            folioForm.elements['total_GST'].value = totalGST.toFixed(2);
        }
        else
            $('#result').html("Record NOT found. Please try again!");
    })
}

var addChargeList = [];

function calculateAddPrice(itemNo, unitPrice){
    var itemName = document.getElementById("minibar_item"+itemNo).value;
    var addQty = parseInt(document.getElementById("add_qty"+itemNo).value);
    var found = false;
    for (var i=0; i<addChargeList.length; i++){
        if (addChargeList[i].item == itemName) {
            found = true;
            addChargeList[i].qty = addQty;
        }
    }

    if (!found){
        var item = {item:itemName, qty:addQty, price:unitPrice};
        addChargeList.push(item);
    }
}

// Get the modal
var modal = document.getElementById("myModal");

// Get the button that opens the modal
var btn = document.getElementById("myBtn");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks the button, open the modal
btn.onclick = function() {
    modal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
    modal.style.display = "none";
    var addTotal = 0;
    var output = "";
    if (addChargeList.length>0){
        for (var i=0; i<addChargeList.length; i++){
            addTotal += addChargeList[i].qty * addChargeList[i].price;
            output += addChargeList[i].item + " - S$" + addChargeList[i].price + " * " + addChargeList[i].qty + "<br>";
        }
        document.getElementById('b_date10').value=document.getElementById('p_date').value;
        document.getElementById("output").innerHTML = output;
        document.getElementById("add_price").value = addTotal.toFixed(2);
        var totalGST = parseFloat(document.getElementById("total").value) + addTotal;
        var totalNoGST = totalGST/1.07;
        document.getElementById("total").value = totalGST.toFixed(2);
        document.getElementById("bal_due").value = totalGST.toFixed(2);
        document.getElementById("total_no_GST").value = totalNoGST.toFixed(2);
        document.getElementById("GST").value = (totalGST-totalNoGST).toFixed(2);
        document.getElementById("total_GST").value = totalGST.toFixed(2);
    }
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}