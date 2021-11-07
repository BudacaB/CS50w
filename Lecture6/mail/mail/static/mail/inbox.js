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
  document.querySelector('#email-view').style.display = 'none';
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
          document.querySelector('#compose-recipients').value = '';
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
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(result => {
    result.forEach(mailDao => {
      const mailDto = document.createElement('div');
      mailDto.className = 'mail';
      if (mailDao.read) {
        mailDto.className = 'mail read';
      }
      mailDto.innerHTML = `<b>${mailDao.sender}</b> &nbsp ${mailDao.subject} <span class="timestamp">${mailDao.timestamp}<span>`;
      mailDto.addEventListener('click', () => {
        if (!mailDao.read) {
          mark_email_read(mailDao.id);
        }
        view_email(mailDao.id, mailbox);
      });
      document.querySelector('#emails-view').append(mailDto);
    });
  })
  .catch(error => console.log('Error', error));
}

function view_email(email_id, mailbox) {
  // Show email view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  fetch(`/emails/${email_id}`)
  .then(response => response.json())
  .then(result => {
    document.querySelector('#email_from').innerHTML = `<b>From:</b> ${result.sender}`;
    document.querySelector('#email_to').innerHTML = `<b>To:</b> ${result.recipients}`;
    document.querySelector('#email_subject').innerHTML = `<b>Subject:</b> ${result.subject}`;
    document.querySelector('#email_timestamp').innerHTML = `<b>Timestamp:</b> ${result.timestamp}`;
    document.querySelector('#email_body').innerHTML = `${result.body}`;
  })
  .catch(error => console.log('Error', error));

  const replyButton = document.querySelector('#reply');
  const archiveButton = document.querySelector('#archive_email');
  const unarchiveButton = document.querySelector('#unarchive_email');
  if (mailbox === 'inbox') {
    replyButton.style.display = "inline-block";
    archiveButton.style.display = 'inline-block';
    unarchiveButton.style.display = 'none';

    archiveButton.addEventListener('click', function archive() {
      archiveEmail(email_id);
      this.removeEventListener('click', archive);
    })

    replyButton.addEventListener('click', function reply() {
      compose_reply_email(email_id);
      this.removeEventListener('click', reply);
    })

  } else if (mailbox === 'archive') {
    replyButton.style.display = 'none';
    archiveButton.style.display = 'none';
    unarchiveButton.style.display = 'inline-block';

    unarchiveButton.addEventListener('click', function unarchive() {
      unarchiveEmail(email_id);
      this.removeEventListener('click', unarchive);
    })
  } else {
    replyButton.style.display = 'none';
    archiveButton.style.display = 'none';
    unarchiveButton.style.display = 'none';
  }
}

function mark_email_read(email_id) {
  fetch(`/emails/${email_id}`, {
    method: 'PUT',
    body: JSON.stringify({
      read: true
    })
  })
  .catch(error => console.log('Error', error));
}

function archiveEmail(email_id) {
  fetch(`/emails/${email_id}`, {
    method: 'PUT',
    body: JSON.stringify({
      archived: true
    })
  })
  .then(response => load_mailbox('inbox'))
  .catch(error => console.log('Error', error));;
}

function unarchiveEmail(email_id) {
  fetch(`/emails/${email_id}`, {
    method: 'PUT',
    body: JSON.stringify({
      archived: false
    })
  })
  .then(response => load_mailbox('inbox'))
  .catch(error => console.log('Error', error));;
}

function compose_reply_email(email_id) {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  fetch(`/emails/${email_id}`)
  .then(response => response.json())
  .then(result => {
    document.querySelector('#compose-recipients').value = result.sender;
    if (result.subject.slice(0, 4) === 'Re: ') {
      document.querySelector('#compose-subject').value = `${result.subject}`;
    } else {
      document.querySelector('#compose-subject').value = `Re: ${result.subject}`;
    }
    document.querySelector('#compose-body').value = `On ${result.timestamp} ${result.sender} wrote:

    ${result.body}`;
  })
  .catch(error => console.log('Error', error));

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
          document.querySelector('#compose-recipients').value = '';
          document.querySelector('#compose-recipients').className = 'form-control';
          this.removeEventListener('click', resetInput);
        });
      }
    })
    .catch(error => console.log('Error', error));
    return false;
  }
}