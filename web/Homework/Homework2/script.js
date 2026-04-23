document.querySelectorAll('.item').forEach(function (item) {
    item.addEventListener('click', function () {
        document.querySelectorAll('.item').forEach(function (el) {
            el.style.backgroundColor = '#c4c0c0';
        });
        item.style.backgroundColor = '#a0a0a0';
    });
});
