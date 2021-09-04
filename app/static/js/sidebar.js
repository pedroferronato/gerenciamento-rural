var menu = document.getElementById("menu")

var side_box = document.getElementById("sidebar_box")

menu.addEventListener('click', () => {
    if (side_box.style.display == '' || side_box.style.display == 'none') side_box.style.display = 'block';
    else side_box.style.display = 'none';
})

side_box.addEventListener('click', (event) => {
    if (event.target.id == side_box.id) side_box.style.display = 'none';
})