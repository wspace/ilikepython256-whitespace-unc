var examples = {
    "Hello, World!": 'MOD.PUSH 0\nMOD.PUSH "!"\nMOD.PUSH "d"\nMOD.PUSH "l"\nMOD.PUSH "r"\nMOD.PUSH "o"\nMOD.PUSH "w"\nMOD.PUSH " "\nMOD.PUSH ","\nMOD.PUSH "o"\nMOD.PUSH "l"\nMOD.PUSH "l"\nMOD.PUSH "e"\nMOD.PUSH "H"\nFLOW.LABL 0\nMOD.DUPE\nFLOW.JMPZ 1\nIO.OUT\nFLOW.JUMP 0\nFLOW.LABL 1\nFLOW.HALT',
    "1 to 10":'MOD.PUSH 1\nFLOW.LABL 0\nMOD.DUPE\nIO.NOUT\nMOD.PUSH 1\nMATH.ADD\nMOD.DUPE\nMOD.PUSH 11\nMATH.SUB\nFLOW.JMPZ 1\nMOD.PUSH "\\n"\nIO.OUT\nFLOW.JUMP 0\nFLOW.LABL 1\nMOD.POP\nFLOW.HALT'
};
var field = document.getElementById("textbox");
function example(name) {
	textbox.value = examples[name];
}
for(var key in examples) {
	document.write("<button onclick='example(\"" + key + "\")'>" + key + "</button>");
}
function fallbackCopyTextToClipboard(text) {
  var textArea = document.createElement("textarea");
  textArea.value = text;
  document.body.appendChild(textArea);
  textArea.focus();
  textArea.select();

  try {
    var successful = document.execCommand('copy');
    var msg = successful ? 'successful' : 'unsuccessful';
    console.log('Fallback: Copying text command was ' + msg);
  } catch (err) {
    console.error('Fallback: Oops, unable to copy', err);
  }

  document.body.removeChild(textArea);
}
function copy(text) {
  if (!navigator.clipboard) {
    fallbackCopyTextToClipboard(text);
    return;
  }
  navigator.clipboard.writeText(text).then(function() {
    console.log('Async: Copying to clipboard was successful!');
    document.getElementById("copied").innerHTML = "Copied!";
    var delay = 150;
    for(var i in [1,2,3,4,5,6,7,8,9,10,11,12,13,14,14.5]) {
    	console.log(i);
    	(function (i) {
    	window.setTimeout (function(){document.getElementById("copied").innerHTML = "<span style='color:rgb(" + i*16 + "," + i*16 + "," + i*16 + ")'>Copied!</span>";}, i*delay);})(i)
    }
    window.setTimeout (function(){document.getElementById("copied").innerHTML = "";}, delay*15);
  }, function(err) {
    console.error('Async: Could not copy text: ', err);
  });
}
