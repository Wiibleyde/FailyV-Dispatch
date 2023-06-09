function randomPos(id) {
    console.log("Un secret est caché dans une position aléatoire du site.")
    let random = Math.floor(Math.random() * 100);
    let random2 = Math.floor(Math.random() * 100);
    document.getElementById(id).style.cssText = "position: absolute;";
    document.getElementById(id).style.top = random + "%";
    document.getElementById(id).style.left = random2 + "%";
    random1sqrt = Math.sqrt(random)
    random2sqrt = Math.sqrt(random2)
    console.log("Position: " + random1sqrt + "%, " + random2sqrt + "%");
}

randomPos("randomPos")