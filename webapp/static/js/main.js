// Closes the flashed messages
let message = document.getElementsByClassName('alert')[0];
let closeMsg = document.getElementById('close-msg');
closeMsg.addEventListener('click', ()=> message.style.display = 'none');
