function edit(postId) {
    document.querySelector(`#post${postId}`).style.display = 'none';
    document.querySelector(`#form${postId}`).removeAttribute('hidden');
}