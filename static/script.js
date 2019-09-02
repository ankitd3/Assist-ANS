let lang__;

var ip = document.getElementById("input-field");
var s = document.getElementById("start-record-btn");
var p = document.getElementById("pause-record-btn");
var languages = document.getElementById("languages");
var submit_btn = document.getElementById("submit-btn");

try {

  var SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  var recognition = new SpeechRecognition();

  recognition.lang = 'en-IN';
}
catch(e) {
  console.error(e);
  $('.no-browser-support').show();
  $('.app').hide();
}

var noteTextarea = $('#note-textarea');
var instructions = $('#recording-instructions');
var notesList = $('ul#notes');

var noteContent = '';

function change_department() {
    document.getElementById("new_department_dropdown").style.display = "block";
    document.getElementById("solution_text").style.display = "none";
}

function filter_dept(dept) {
  var divsToHide = document.getElementsByClassName(dept); //divsToHide is an array
    for(var i = 0; i < divsToHide.length; i++){
        //divsToHide[i].style.visibility = "hidden"; // or
        divsToHide[i].style.display = "block"; // depending on what you're doing
    }
    console.log(divsToHide.length)
    document.getElementById("department_dropdown").style.display = "none";
}

function select_query(q_id) {
  
  document.getElementById("solve_form").style.display = "block";
  console.log(document.getElementById("solve_form").style.display)
  document.getElementById("query_id_input").value = q_id;
  document.body.scrollTop = 0;
  document.documentElement.scrollTop = 0;
}

function change_language(lang_) {
  lang__ = lang_;
  languages.style.display = "none";
  ip.style.display = "block";
  s.style.display = "block";
  p.style.display = "block";
  submit_btn.style.display = "block";
  instructions.text('Please press start record button and allow access to microphone.');
}
$('#satisfied').on('click', function(e) {
  ip.style.display = "block";
  submit_btn.style.display = "block";
  languages.style.display = "none";
  instructions.text('Please select "submit" button to proceed');
});
$('#submit-btn').on('click', function(e) {
  s.style.display = "none";
  p.style.display = "none";
  ip.style.display = "none";
  submit_btn.style.display = "none";
  languages.style.display = "none";
  instructions.text("ML in Action...");

});
/*-----------------------------
      Voice Recognition 
------------------------------*/

// If false, the recording will stop after a few seconds of silence.
// When true, the silence period is longer (about 15 seconds),
// allowing us to keep recording even when the user pauses. 
recognition.continuous = true;

// This block is called every time the Speech APi captures a line. 
recognition.onresult = function(event) {

  // event is a SpeechRecognitionEvent object.
  // It holds all the lines we have captured so far. 
  // We only need the current one.
  var current = event.resultIndex;

  // Get a transcript of what was said.
  var transcript = event.results[current][0].transcript;

  // Add the current transcript to the contents of our Note.
  // There is a weird bug on mobile, where everything is repeated twice.
  // There is no official solution so far so we have to handle an edge case.
  var mobileRepeatBug = (current == 1 && transcript == event.results[0][0].transcript);

  if(!mobileRepeatBug) {
    noteContent += transcript;
    noteTextarea.val(noteContent);
  }
};

recognition.onstart = function() { 
  instructions.text('Voice recognition activated. Try speaking into the microphone.');
}

recognition.onspeechend = function() {
  instructions.text('You were quiet for a while so voice recognition turned itself off.');
}

recognition.onerror = function(event) {
  if(event.error == 'no-speech') {
    instructions.text('No speech was detected. Try again.');  
  };
}

/*-----------------------------
      App buttons and input 
------------------------------*/

$('#start-record-btn').on('click', function(e) {
  if (noteContent.length) {
    noteContent += ' ';
  }
  recognition.lang = lang__;
  recognition.start();
});


$('#pause-record-btn').on('click', function(e) {
  recognition.stop();
  instructions.text('Voice recognition paused.');
});

// Sync the text inside the text area with the noteContent variable.
noteTextarea.on('input', function() {
  noteContent = $(this).val();
})


notesList.on('click', function(e) {
  e.preventDefault();
  var target = $(e.target);

  // Listen to the selected note.
  if(target.hasClass('listen-note')) {
    var content = target.closest('.note').find('.content').text();
    readOutLoud(content);
  }

});
/*-----------------------------
      Speech Synthesis 
------------------------------*/

function readOutLoud(message) {
	var speech = new SpeechSynthesisUtterance();

  // Set the text and voice attributes.
	speech.text = message;
	speech.volume = 1;
	speech.rate = 1;
	speech.pitch = 1;
  
	window.speechSynthesis.speak(speech);
}