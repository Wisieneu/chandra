
// expands the reply div with "replying to X" when it's focused

const textAreaState = document.querySelector('.comment-textarea').addEventListener('focus', function() {
    replyingTo.classList.remove('inactive')
  });

// selectors

const replyingTo = document.querySelector('.replying-to')
const textArea = document.querySelector('.comment-textarea')
const button = document.querySelector('.comment-btn-active')


// resizes the text area automatically as the text gets longer

textArea.addEventListener('input', autoResize, false);
          
    function autoResize() {
        this.style.height = 'auto';
        this.style.height = this.scrollHeight + 'px';
    }

// prevents the button from being clicked when the value is empty or full of white space

    textArea.addEventListener("input", function() {
      if (textArea.value.trim() !== "") {
        button.classList.remove("comment-btn-inactive");
      } else {
        button.classList.add("comment-btn-inactive");
      }
    });
 
// adds a limit of 100 characters per comment

    textArea.addEventListener("input", function() {
      if (textArea.value.length > 100) {
        textArea.value = textArea.value.slice(0, 100);
      }
    });

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