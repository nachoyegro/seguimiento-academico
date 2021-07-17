

document.querySelector("html").classList.add('js');

var fileInput = document.querySelector(".input-file"),
    button = document.querySelector(".input-file-trigger"),
    fileSelected = document.querySelector(".file-selected");

var cargarButton = document.getElementById("cargarButton");
var spinner = document.getElementById("spinner");
var userFeedback = document.getElementById("userFeedback");
    

button.addEventListener("keydown", function (event) {
    if (event.keyCode == 13 || event.keyCode == 32) {
        fileInput.focus();
    }
});

button.addEventListener("click", function (event) {
    fileInput.focus();
    return false;
});

fileInput.addEventListener("change", function (event) {
    if(event.target.files.length > 0){
        fileSelected.value = event.target.files[0].name;
        fileSelected.hidden = false;
        cargarButton.hidden = false;
    }

});

cargarButton.addEventListener("click", function (event) {
    spinner.hidden = false;
    userFeedback.hidden = true;
    cargarButton.hidden = true;
});

userFeedback.addEventListener("change", function (event) {
    spinner.hidden = !userFeedback.hidden;
});

