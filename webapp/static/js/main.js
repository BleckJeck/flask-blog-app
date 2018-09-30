// Closes the flashed messages
let message = document.getElementsByClassName('alert')[0];
if(message) {
  let closeMsg = document.getElementById('close-msg');
  closeMsg.addEventListener('click', ()=> message.style.display = 'none');
}

