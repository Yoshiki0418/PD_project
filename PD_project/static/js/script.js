document.addEventListener('DOMContentLoaded', function() {
    const items = document.querySelectorAll('.item1');
    
    items.forEach(item => {
        const daysLeft = item.getAttribute('data-days-left');
        const isPresent = item.getAttribute('data-is-present');
        const circle = item.querySelector('.circle');
        const circle2 = item.querySelector('.date-circle');

        if (daysLeft === '不明') {
            if (isPresent === '1') {
                circle.style.backgroundColor = 'blue';
                circle2.style.backgroundColor = 'blue';
            } else {
                circle.style.backgroundColor = 'gray';
                circle2.style.backgroundColor = 'gray';
            }
        } else if (parseInt(daysLeft) <= 7) {
            circle.style.backgroundColor = 'red';
            circle2.style.backgroundColor = 'red';
        } else {
            circle.style.backgroundColor = 'green';
            circle2.style.backgroundColor = 'green';
        }
    });
});

document.addEventListener('DOMContentLoaded', function() {
    const items = document.querySelectorAll('.item');
    
    items.forEach(item => {
        const daysLeft = item.getAttribute('data-days-left');
        const isPresent = item.getAttribute('data-is-present');
        const circle = item.querySelector('.circle');

        if (daysLeft === '不明') {
            if (isPresent === '1') {
                circle.style.backgroundColor = 'blue';
            } else {
                circle.style.backgroundColor = 'gray';
            }
        } else if (parseInt(daysLeft) <= 7) {
            circle.style.backgroundColor = 'red';
        } else {
            circle.style.backgroundColor = 'green';
        }
    });
});