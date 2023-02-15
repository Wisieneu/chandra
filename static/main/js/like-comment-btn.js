"use strict";

const isAuth = JSON.parse(document.getElementById("isAuth").textContent);
const modal = document.querySelector(".modal");
const overlay = document.querySelector(".overlay");
const closeButton = document.querySelector(".modal-close-button");
const postsDiv = document.getElementById("infinite-container"); // getting the HTMl element

function changeLikeStatus(postID) {
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
    ).innerHTML = `<i class='button-like-post fa-regular fa-heart' onclick=changeLikeStatus(${postID})></i> <span class="likes-count">${serverResponse.likes_amount}</span>`;
  };
  postLikeXHR.send();
}

function showModal() {
  modal.classList.remove("invisible");
  overlay.classList.remove("invisible");
}

function closeModal() {
  modal.classList.add("invisible");
  overlay.classList.add("invisible");
}
