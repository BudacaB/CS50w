document.addEventListener('DOMContentLoaded', function() {
    getPosts();
})

function getPosts() {
    fetch('/all_posts')
    .then(response => response.json())
    .then(result => {
        console.log(result)
        const postsDiv = document.querySelector('#posts');
        result.forEach(element => {
            postsDiv.innerHTML += 
                `<div class="card post">
                    <div class="card-body">
                        <div class="row">
                            <div class="col-12">
                                <h5>${element.user}</h5>
                                <p>${element.post}</p>
                                <p>${element.created}</p>
                                <button class="heart" onclick="clicked(this)" id="${element.user}${element.id}">&hearts;</button>
                                <span>${element.likes}</span>
                            </div>
                        </div>
                    </div>
                </div>`
            // add listener upon creation so on click will fire on the first click
            const button = document.querySelector(`#${element.user}${element.id}`);
            button.addEventListener('click', clicked);
        });
    })
    .catch(error => console.log('Error', error));
}

function clicked(elem) {
    if (elem.className == 'heart') {
        elem.className = 'heart red_heart';
    } else {
        elem.className = 'heart';
    }
}