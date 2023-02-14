
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