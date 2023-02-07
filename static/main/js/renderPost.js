const postsDiv = document.getElementById("infinite-container") // getting the HTMl element
postsDiv.innerHTML = 'Loading...' // setting the HTML content inside the element 



const xhr = new XMLHttpRequest();
const method = 'GET';
const url = 'json/posts/all';
const responseType = 'json';

function handleDidLike (postID, currentCount) {
    console.log(postID, currentCount)
}

function likeButton (post) {
    return `<button class='buttonlikejakisidk' onclick=handleDidLike(${post.id},${post.likes_count})>Like</button>`
}


function formatPost (post) {
    authorRef = (post.author.username == post.author.display_name) ? `@${post.author.username}` : authorRef = `${post.author.display_name} <span id='greyed-out-tag-name-span'>@${post.author.username}</span>`
    
    // if (post.author.username == post.author.display_name) {
    //     let authorRef = `@${post.author.username}`
    // } else {
    //     let authorRef = `${post.author.display_name} <span id='greyed-out-tag-name-span'>@${post.author.username}</span>`
    // } WHY DOES THIS NOT WORK??


    // onclick="location.href='/post/${post.id}'" paste it back into the first div after likes are done
    let formattedPost = `<div class="post-wrapper infinite-item" id="post-${post.id}" style="cursor: pointer;">
    <a class="PLACEHOLDER" href="profile/${post.author.username}"><img class="post-image" src="${post.author.pfp_url}"></a>
    <div class="name-date">
        <a class="post-nickname" href="profile/${post.author.username}">${authorRef}</a>
        <small class="PLACEHOLDER">${post.date_posted}</small>
    </div>
    <p class="post-content" >${post.content}</p>
    <div class="PLACEHOLDER buttonlikejakisidk">
        ${likeButton(post)}
    </div>
</div>`
    return formattedPost
}


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