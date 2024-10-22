document.addEventListener('DOMContentLoaded', function() {
    const urlBar = document.getElementById('url-bar');
    const goButton = document.getElementById('go-button');
    const backButton = document.getElementById('back-button');
    const forwardButton = document.getElementById('forward-button');
    const refreshButton = document.getElementById('refresh-button');
    const homeButton = document.getElementById('home-button');
    const bookmarkButton = document.getElementById('bookmark-button');

    goButton.addEventListener('click', () => navigate());
    urlBar.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            navigate();
        }
    });

    backButton.addEventListener('click', () => window.history.back());
    forwardButton.addEventListener('click', () => window.history.forward());
    refreshButton.addEventListener('click', () => window.location.reload());
    homeButton.addEventListener('click', () => navigate('http://www.google.com'));
    bookmarkButton.addEventListener('click', () => console.log('Bookmark clicked'));

    function navigate(url) {
        url = url || urlBar.value;
        if (typeof url === 'string' && url.trim() !== '') {
            if (!url.startsWith('http://') && !url.startsWith('https://')) {
                url = 'http://' + url;
            }
            window.pywebview.api.navigate(url);
        }
    }
});
