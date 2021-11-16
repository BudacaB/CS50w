document.addEventListener('DOMContentLoaded', function() {
    // const whiteHeart = '\u2661';
    // const blackHeart = '\u2764';
    // const button = document.querySelector('.heart');
    // button.addEventListener('click', function toggle() {
    //     console.log('clicked');
    //     const like = button.textContent;
    //     if(like==whiteHeart) {
    //         button.textContent = blackHeart;
    //         button.className = 'red_heart';
    //     } else {
    //         button.textContent = whiteHeart;
    //         button.className = '';
    //     }
    // });

    fetch('/all_posts')
    .then(response => response.json())
    .then(result => {
        console.log(result)
        const postsDiv = document.querySelector('#posts');
        result.forEach(element => {
            console.log(element);
            // const post = document.createElement('div');
            // post.innerHTML = "test";
            postsDiv.innerHTML += `<div class="card post">
            <div class="card-body">
                <div class="row">
                    <div class="col-12">
                        <h5>${element.user}</h5>
                        <p>${element.post}</p>
                        <p>${element.created}</p>
                        <button class="heart">&#9825;</button>
                        <span>${element.likes} likes</span>
                    </div>
                </div>
            </div>
        </div>`
            // postsDiv.append(post);
        });
    })
    .catch(error => console.log('Error', error));
})