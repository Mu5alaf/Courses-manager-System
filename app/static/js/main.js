document.addEventListener('DOMContentLoaded', function () {
    const tabs = document.querySelectorAll('.nav-tab');
    const contents = document.querySelectorAll('.tab-content');

    tabs.forEach(tab => {
        tab.addEventListener('click', function (e) {
            e.preventDefault();

            // Remove active class from all tabs and contents
            tabs.forEach(t => t.classList.remove('active'));
            contents.forEach(c => c.classList.remove('active'));

            // Add active class to the clicked tab
            this.classList.add('active');

            // Add active class to the corresponding tab content
            const target = this.getAttribute('data-target');
            const content = document.querySelector(target);
            if (content) {
                content.classList.add('active');
            }
        });
    });
});
