document.addEventListener('DOMContentLoaded', function() {
    const currentPath = window.location.pathname;        
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
    });    
    document.querySelectorAll('.nav-link').forEach(link => {
        if(link.href === window.location.href) {
            link.classList.add('active');
        }
    });
});