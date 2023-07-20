function interDropdown(id) {
    $("#interDrop" + id).toggleClass("show")
}

function affiliationDropdown(id) {
    $("#affiliationDrop" + id).toggleClass("show")
}

$(document).on("click", function(event) {
    if (!$(event.target).closest(".dropbtn").length) {
        $(".dropdown-content.show").removeClass("show")
    }
})