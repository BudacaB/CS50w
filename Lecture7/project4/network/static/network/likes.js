function clicked(elem) {
    if (elem.className == 'heart') {
        elem.className = 'heart red_heart';
    } else {
        elem.className = 'heart';
    }
}