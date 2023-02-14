'use strict';

const isAuth = JSON.parse(document.getElementById('isAuth').textContent);
const modal = document.querySelector('.modal');
const overlay = document.querySelector('.overlay');
const closeButton = document.querySelector('.modal-close-button')
const postsDiv = document.getElementById("infinite-container") // getting the HTMl element
postsDiv.innerHTML = 'Loading...' // setting the HTML content inside the element 



function changeLikeStatus (postID) {
    const postLikeXHR = new XMLHttpRequest();
    postLikeXHR.open('POST', `/like/${postID}`, true);
    // get the csrf token to be able to make changes in the database
    const csrf_token = document.cookie.match(/csrftoken=(\w+)/)[1]; 
    postLikeXHR.setRequestHeader("X-CSRFToken", csrf_token);
    postLikeXHR.onload = function () {
        const serverResponse = JSON.parse(postLikeXHR.response)
        console.log(serverResponse)
        const postDiv = document.getElementById(`post-${postID}`)
        postDiv.querySelector('.like-button-container').innerHTML = `<button class='button-like-post' onclick=changeLikeStatus(${postID})>${serverResponse.likes_count} Likes</button>`
    }
    postLikeXHR.send();

    // change current like button styling
}

function showModal() {
    modal.classList.remove('invisible')
    overlay.classList.remove('invisible')
    
}

function closeModal() {
    modal.classList.add('invisible')
    overlay.classList.add('invisible')
}


function likeButton (post, isAuthenticated = isAuth) {
    if (isAuthenticated) {
        return `<button class='button-like-post' onclick=changeLikeStatus(${post.id})>${post.likes_count} Likes </button>`
    } else {
        return `<button class='button-like-post' onclick=showModal()> ${post.likes_count} Likes </button>`
    }
}




function formatPost (post) {
    console.log(post)
    const authorRef = (post.author.username == post.author.display_name) ? `${post.author.username}` : `${post.author.display_name} <span id='greyed-out-tag-name-span'>@${post.author.username}</span>`
    let formattedPost = `<div class="post-wrapper infinite-item" id="post-${post.id}" style="cursor: pointer;">
    <a class="PLACEHOLDER" href="profile/${post.author.username}"><img class="post-image" src="${post.author.pfp_url}"></a>
    <div class="name-date">
        <a class="post-nickname" href="profile/${post.author.username}">${authorRef}</a>
        <small class="PLACEHOLDER">${post.date_posted}</small>
    </div>
    <p class="post-content" >${post.content}</p>
    <div class="like-button-container">
        ${likeButton(post)}
    </div>
</div>`
    return formattedPost
}

const xhr = new XMLHttpRequest();
const method = 'GET';
const url = 'json/posts/all';
const responseType = 'json';

xhr.responseType = responseType;
xhr.open(method, url);
xhr.onload = function () {
    const serverResponse = xhr.response
    let listedItems = serverResponse.response
    let finalPostStr = ''
    for (let i = 0; i<12; i++) {
        let post = listedItems[i]
        let currentItem = formatPost(post)
        finalPostStr += currentItem
    }
    postsDiv.innerHTML = finalPostStr
}
xhr.send()

window.onscroll = function() {
    if ((window.innerHeight + Math.ceil(window.pageYOffset)) >= document.body.offsetHeight) {
        alert('At the bottom!')
        
        const xhr = new XMLHttpRequest();
        

        xhr.responseType = 'json';
        xhr.open('GET', 'json/posts/all');
        xhr.onload = function () {
            const nextPostDiv = document.getElementById("next-post")
            const serverResponse = xhr.response
            let listedItems = serverResponse.response
            let finalPostStr = ''
            let nextPostNumber = parseInt(nextPostDiv.innerHTML)

            for (nextPostNumber; nextPostNumber<listedItems.length; nextPostNumber++) {
                console.log(nextPostNumber, listedItems.length)
                console.log(listedItems[nextPostNumber])
                let post = listedItems[nextPostNumber]
                if (post == undefined){
                    end = document.getElementById('ending-tag')
                    end.classList.remove('invisible')
                    break
                }
                let currentItem = formatPost(post)
                finalPostStr += currentItem
            }
            766                                         
            if (nextPostNumber+1 == listedItems.length) {
                end = document.getElementById('ending-tag')
                end.classList.remove('invisible')
            }
            nextPostDiv.innerHTML = nextPostNumber += 9
            postsDiv.innerHTML += finalPostStr

        }
        xhr.send()
    }
  }