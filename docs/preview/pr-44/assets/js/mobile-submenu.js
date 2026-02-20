

function toggleSubmenu(){
    // class = masthead__menu-item has-submenu
    submenuLists = document.querySelectorAll('.masthead__menu-item.has-submenu');
    hamburgerButtons = document.querySelectorAll('.greedy-nav__toggle')[0];

    submenuLists.forEach(function(submenuList){
        submenuList.addEventListener('click', function(event){
            event.stopPropagation();
            submenuList.classList.toggle('submenuExpanded');
        });
    });

}

toggleSubmenu();