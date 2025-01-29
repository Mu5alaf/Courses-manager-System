window.addEventListener("load", function() {
    const video = document.getElementById('video-player-element');
    const emojiPopup = document.getElementById('emoji-congratulations');
    const userName = document.getElementById('user-name');
    const contentContainer = document.querySelector('.container'); 

    video.addEventListener('ended', function() {
        contentContainer.classList.add('course-container-blur');

        emojiPopup.style.display = 'block';
        userName.style.display = 'block';

        setTimeout(function() {
            emojiPopup.style.display = 'none';
            contentContainer.classList.remove('course-container-blur');
        }, 2000);
    });
});

