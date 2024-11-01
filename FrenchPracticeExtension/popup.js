const newsApiUrl = 'https://api.rss2json.com/v1/api.json?rss_url=https://www.lemonde.fr/rss/une.xml';
const youtubePlaylistId = 'PLmK-vbXTxuypeIF5rXp_MlI9SkXcNQacV';

function fetchNewsSnippet() {
    fetch(newsApiUrl)
        .then(response => response.json())
        .then(data => {
            // Get all articles
            const items = data.items;
            if (items && items.length > 0) {
                // Select a random article
                const randomIndex = Math.floor(Math.random() * items.length);
                const selectedArticle = items[randomIndex];

                const snippet = selectedArticle.title;
                const snippetLink = selectedArticle.link;
                document.getElementById('news-snippet').innerHTML = `<a href="${snippetLink}" target="_blank">${snippet}</a>`;
            } else {
                document.getElementById('news-snippet').innerText = "No news available";
            }
        })
        .catch(error => {
            console.error('Error fetching news snippet:', error);
            document.getElementById('news-snippet').innerText = 'Erreur lors de la récupération des nouvelles.';
        });
}

function getRandomVideo() {
    // Create a random index based on the number of videos in the playlist
    const totalVideos = 15; // Update this with the actual number of videos in your playlist
    const randomIndex = Math.floor(Math.random() * totalVideos);
    const videoUrl = `https://www.youtube.com/embed?list=${youtubePlaylistId}&index=${randomIndex}`;
    document.getElementById('youtube-video').src = videoUrl;
}

document.addEventListener('DOMContentLoaded', () => {
    fetchNewsSnippet();
    getRandomVideo();
});
