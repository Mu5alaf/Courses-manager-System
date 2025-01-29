document.addEventListener('DOMContentLoaded', function () {
    const tabs = document.querySelectorAll('.nav-tab');
    const contents = document.querySelectorAll('.tab-content');

    tabs.forEach(tab => {
        tab.addEventListener('click', function (e) {
            e.preventDefault();

            tabs.forEach(t => t.classList.remove('active'));
            contents.forEach(c => c.classList.remove('active'));

            this.classList.add('active');

            const target = this.getAttribute('data-target');
            const content = document.querySelector(target);
            if (content) {
                content.classList.add('active');
            }
        });
    });
});
