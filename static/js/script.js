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
        } else if (parseInt(daysLeft) <= 4) {
            circle.style.backgroundColor = 'red';
            circle2.style.backgroundColor = 'red';
        } else {
            circle.style.backgroundColor = 'green';
            circle2.style.backgroundColor = 'green';
        }
    });
});

document.addEventListener('DOMContentLoaded', function() {
    const items = document.querySelectorAll('.item2');
    
    items.forEach(item => {
        const daysLeft = item.getAttribute('data-days-left');
        const isPresent = item.getAttribute('data-is-present');
        const circle = item.querySelector('.circle');
        const circle2 = item.querySelector('.date-circle');
        const circle3 = item.querySelector('.edit-circle');

        if (daysLeft === '不明') {
            if (isPresent === '1') {
                circle.style.backgroundColor = 'blue';
                circle2.style.backgroundColor = 'blue';
                circle3.style.backgroundColor = 'blue';
            } else {
                circle.style.backgroundColor = 'gray';
                circle2.style.backgroundColor = 'gray';
                circle3.style.backgroundColor = 'gray';
            }
        } else if (parseInt(daysLeft) <= 4) {
            circle.style.backgroundColor = 'red';
            circle2.style.backgroundColor = 'red';
            circle3.style.backgroundColor = 'red';
        } else {
            circle.style.backgroundColor = 'green';
            circle2.style.backgroundColor = 'green';
            circle3.style.backgroundColor = 'green';
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
        } else if (parseInt(daysLeft) <= 4) {
            circle.style.backgroundColor = 'red';
        } else {
            circle.style.backgroundColor = 'green';
        }
    });
});