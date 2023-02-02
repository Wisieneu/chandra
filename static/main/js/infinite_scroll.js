// API utilizaiton (for potential future use)
/*
const postsElement = document.getElementById('posts-wrapper'); 
console.log(document.querySelector('.posts-wrapper'))
postsElement.innerHTML = 'Loading...';

const xhr = new XMLHttpRequest();
const method = 'GET';
const url = '/posts/json/all';
const responseType = 'json';

xhr.responseType = responseType;
xhr.open(method, url);
console.log('test');
xhr.onload = function () {
  const serverResponse = xhr.response;
  var listedItems = serverResponse.response; // array of posts
  console.log(listedItems);
  var finalPostStr = ''
  for (let i = 0; i < listedItems.length; i++) {
    
}
};
xhr.send();

function handleDidLike (postID, currentCount) {
  currentCount++
  return 
}

function likeBtn (post) {
  return "<button class='btn btn-primary' onclick=handleDidLike("+post.id+", "+post.likes+")>"+post.likes+" Likes</button>";
};
*/

// Infinite scrolling functionality
var infinite = new Waypoint.Infinite({
  element: $('.infinite-container')[0],

  offset: 'bottom-in-view',

  onBeforePageLoad: function () {
      $('.loading').show();
  },
  onAfterPageLoad: function () {
      $('.loading').hide();
  }

});