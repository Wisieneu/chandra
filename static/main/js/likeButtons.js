"use strict";

const modal = document.querySelector(".modal-not-logged-in");
const overlay = document.querySelector(".overlay");
const closeButton = document.querySelector(".modal-close-button");


function showModal() {
  modal.classList.remove("invisible");
  overlay.classList.remove("invisible");
}

function closeModal() {
  modal.classList.add("invisible");
  overlay.classList.add("invisible");
}

function changePostLikeStatus(postID) {
  const postLikeXHR = new XMLHttpRequest();
  postLikeXHR.open("POST", `/like/${postID}`, true);
  // get the csrf token to be able to make changes in the database
  const csrf_token = document.cookie.match(/csrftoken=(\w+)/)[1];
  postLikeXHR.setRequestHeader("X-CSRFToken", csrf_token);
  postLikeXHR.onload = function () {
    const serverResponse = JSON.parse(postLikeXHR.response);
    const postDiv = document.getElementById(`post-${postID}`);
    postDiv.querySelector(
      ".like-button-container"
    ).innerHTML = `<i class='button-like-post fa-regular fa-heart' onclick=changePostLikeStatus(${postID})></i> <span class="likes-count">${serverResponse.likes_amount}</span>`;
  };
  postLikeXHR.send();
}

function changeCommentLikeStatus(commentID) {
  const commentLikeXHR = new XMLHttpRequest();
  commentLikeXHR.open("POST", `/likecomment/${commentID}`, true);
  // get the csrf token to be able to make changes in the database
  const csrf_token = document.cookie.match(/csrftoken=(\w+)/)[1];
  commentLikeXHR.setRequestHeader("X-CSRFToken", csrf_token);
  commentLikeXHR.onload = function () {
    const serverResponse = JSON.parse(commentLikeXHR.response);
    const commentDiv = document.getElementById(`comment-${commentID}`);
    commentDiv.querySelector(
      ".like-button-container"
    ).innerHTML = `<i class="button-like-comment fa-regular fa-heart" onclick="changeCommentLikeStatus(${commentID})"></i> <span class="likes-count">${serverResponse.likes_amount}</span>`;
  };
  commentLikeXHR.send();
}