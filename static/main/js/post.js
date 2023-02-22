// selectors

const textArea = document.getElementById('id_content');
const button = document.querySelector('.post-create-btn-active');
const img = document.getElementById('img-preview')

// resizes the text area automatically as the text gets longer

textArea.addEventListener('input', autoResize, false);
function autoResize() {
    this.style.height = this.scrollHeight + 'px';
}

// prevents the button from being clicked when the value is empty or full of white space

textArea.addEventListener("input", function () {
    if (textArea.value.trim() !== "") {
        button.classList.remove("post-create-btn-inactive");
    } else {
        button.classList.add("post-create-btn-inactive");                           
    }
});

