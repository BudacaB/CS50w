document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  
  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  // POST the email
  document.querySelector('form').onsubmit = function() {
    const recipients = document.querySelector('#compose-recipients').value
    const subject = document.querySelector('#compose-subject').value
    const body = document.querySelector('#compose-body').value
    
    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
          recipients: recipients,
          subject: subject,
          body: body
      })
    })
    .then(response => {
      if (response.status === 201) {
        load_mailbox('sent');
      } else if (response.status === 400) {
        document.querySelector('#compose-recipients').value = 'This user does not exist';
        document.querySelector('#compose-recipients').className = 'form-control send';
        document.querySelector('#compose-recipients').addEventListener('click', function resetInput() {
          compose_email();
          document.querySelector('#compose-recipients').className = 'form-control';
          this.removeEventListener('click', resetInput);
        });
      }
    })
    .catch(error => console.log('Error', error));
    return false;
  }
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(result => {
    result.forEach(element => {
      console.log(element);
      const mail = document.createElement('div');
      mail.setAttribute('id', 'mail');
      mail.innerHTML = `<b>${element.sender}</b> &nbsp ${element.subject} <span id="timestamp">${element.timestamp}<span>`;
      document.querySelector('#emails-view').append(mail);
    });
  });


}