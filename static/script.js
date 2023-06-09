function interDropdown(id) {
    $("#interDrop" + id).toggleClass("show")
}

function salleDropdown(id) {
    $("#salleDrop" + id).toggleClass("show")
}

$(document).on("click", function(event) {
    if (!$(event.target).closest(".dropbtn").length) {
        $(".dropdown-content.show").removeClass("show")
    }
})
