function edit(postId) {
    document.querySelector(`#post${postId}`).style.display = 'none';
    document.querySelector(`#form${postId}`).removeAttribute('hidden');
}

function saveEdit(postId) {
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
    
}