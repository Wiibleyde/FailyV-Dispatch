function interDropdown(id) {
    let element = document.getElementById("interDrop" + id) 
    if (element.classList.contains("show")) {
        element.classList.remove("show")
    } else {
        element.classList.add("show")
    }
}

function salleDropdown(id) {
    let element = document.getElementById("salleDrop" + id) 
    if (element.classList.contains("show")) {
        element.classList.remove("show") 
    } else {
        element.classList.add("show") 
    }
}

document.addEventListener("click", function (event) {
    let target = event.target 
    let dropbtn = target.closest(".dropbtn") 
    if (!dropbtn) {
        let dropdowns = document.querySelectorAll(".dropdown-content.show") 
        for (let i = 0; i < dropdowns.length; i++) {
            dropdowns[i].classList.remove("show") 
        }
    }
}) 