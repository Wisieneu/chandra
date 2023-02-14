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
        postDiv.querySelector('.like-button-container').innerHTML = `<i class='button-like-post fa-regular fa-heart' onclick=changeLikeStatus(${postID})></i> <span class="likes-count">${serverResponse.likes_count}</span>`

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
        return `<i class='button-like-post fa-regular fa-heart' onclick=changeLikeStatus(${post.id})></i> <span class="likes-count">${post.likes_count}</span>`
    } else {
        return `<i class='button-like-post fa-regular fa-heart' onclick=showModal()> </i> <span class="likes-count">${post.likes_count}</span>`
    }
}




function formatPost (post) {
    const authorRef = (post.author.username == post.author.display_name) ? `${post.author.username}` : `${post.author.display_name} <span id='greyed-out-tag-name-span'>@${post.author.username}</span>`
    let formattedPost = `
        <div class="post-wrapper infinite-item" id="post-${post.id}">

        <div class="main-page-post-wrapper" style="cursor: pointer;" onclick="location.href='/post/${ post.id }';">
            <a class="PLACEHOLDER" href="profile/${post.author.username}"><img class="post-image" src="${post.author.pfp_url}"></a>
            <div class="name-date">
                <a class="post-nickname" href="profile/${post.author.username}">${authorRef}</a>
                <small class="PLACEHOLDER">${post.date_posted}</small>
                <p class="post-content" >${post.content}</p>
            </div>
            
        </div>
        <div class="like-button-container">
            ${likeButton(post)}
        </div>
        </div>
        
    `
    return formattedPost
}

const xhr = new XMLHttpRequest();
const method = 'GET';
const url = 'json/posts/all';
const responseType = 'json';

xhr.responseType = responseType;
xhr.open(method, url);
xhr.onload = function () {
    console.log(xhr.response)
    const serverResponse = xhr.response
    let listedItems = serverResponse.response
    let finalPostStr = ''
    for (let i = 0; i<listedItems.length; i++) {
        let post = listedItems[i]
        let currentItem = formatPost(post)
        finalPostStr += currentItem
    }
    postsDiv.innerHTML = finalPostStr
}
xhr.send()

