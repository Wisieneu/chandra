const imageInput = document.getElementById('img-input')
const imagePreview = document.getElementById('img-preview')

imageInput.onchange = evt => {
    const [file] = imageInput.files
    if (file) {
      imagePreview.src = URL.createObjectURL(file)
    }
  }