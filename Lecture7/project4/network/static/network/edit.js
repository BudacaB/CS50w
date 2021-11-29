function editIndex(postId) {
    document.querySelector(`#post${postId}`).style.display = 'none';
    document.querySelector(`#form${postId}`).removeAttribute('hidden');
}

function editProfile(postId) {
    document.querySelector(`#profilePost${postId}`).style.display = 'none';
    document.querySelector(`#profileForm${postId}`).removeAttribute('hidden');
}

function saveEdit(postId, location) {
    if (location == '') {
        let updatedPost = document.querySelector(`#textarea${postId}`).value;
        fetch(`/update/${postId}`, {
            method: 'PUT',
            body: JSON.stringify({
                post: updatedPost
            })
          })
          .then(response => response.json())
          .then(result => {
            document.querySelector(`#post${postId}`).innerHTML = result.updatedPost;
            document.querySelector(`#post${postId}`).style.display = 'block';
            document.querySelector(`#form${postId}`).hidden = true;
          })
          .catch(error => console.log('Error', error));
    } else {
        let updatedPost = document.querySelector(`#profileTextarea${postId}`).value;
        fetch(`/update/${postId}`, {
            method: 'PUT',
            body: JSON.stringify({
                post: updatedPost
            })
          })
          .then(response => response.json())
          .then(result => {
            document.querySelector(`#profilePost${postId}`).innerHTML = result.updatedPost;
            document.querySelector(`#profilePost${postId}`).style.display = 'block';
            document.querySelector(`#profileForm${postId}`).hidden = true;
          })
          .catch(error => console.log('Error', error));
    }
}