console.log("hi");

let bookmarks = document.getElementById('bookmarks');
let mark = document.getElementById('mark');

mark.addEventListener('click', () => {
 if(bookmarks.classList.contains('bookmarks-green')){
    bookmarks.classList.remove('bookmarks-green');
    console.log('emove');
 } else {
   bookmarks.classList.add('bookmarks-green');
   console.log('add');
 }


  console.log("hi");
});
