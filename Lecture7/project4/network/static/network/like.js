function like(elem, user, postId) {
    if (elem.className == 'heart') {
        fetch(`/like/${postId}/${user}`, {
            method: 'POST'
          })
          .catch(error => console.log('Error', error));
        let likes = parseInt(document.querySelector(`#like${postId}`).innerHTML);
        document.querySelector(`#like${postId}`).innerHTML = likes + 1;
        elem.className = 'heart red_heart';
    } else {
        fetch(`/like/${postId}/${user}`, {
            method: 'POST'
          })
          .catch(error => console.log('Error', error));
        let likes = parseInt(document.querySelector(`#like${postId}`).innerHTML);
        document.querySelector(`#like${postId}`).innerHTML = likes - 1;
        elem.className = 'heart';
    }
}