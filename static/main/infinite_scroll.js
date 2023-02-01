// Infinite scrolling functionality
const postsElement = document.getElementById('posts-wrapper');
console.log(document.querySelector('.posts-wrapper'))
postsElement.innerHTML = 'Loading...';

const xhr = new XMLHttpRequest();
const method = 'GET';
const url = '/posts/json/all';
const responseType = 'json';

xhr.responseType = responseType
xhr.open(method, url);
console.log('test');
xhr.onload = function () {
  console.log('test');
  console.log(xhr.response);
  const serverResponse = xhr.response;
  var listedItems = serverResponse.response;
}
xhr.send()