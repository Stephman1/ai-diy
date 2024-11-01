const headlineElement = document.getElementById('headline');
const videoFrame = document.getElementById('videoFrame');
const newContentButton = document.getElementById('newContent');

// Playlist URL for the Piece of French channel
const PLAYLIST_URL = 'https://www.youtube.com/playlist?list=PLmK-vbXTxuypeIF5rXp_MlI9SkXcNQacV';

async function fetchReadingContent() {
  try {
    const response = await fetch("https://api.rss2json.com/v1/api.json?rss_url=https://www.lemonde.fr/rss/une.xml");
    const data = await response.json();

    if (data.items && data.items.length > 0) {
      const randomIndex = Math.floor(Math.random() * data.items.length);
      const headline = data.items[randomIndex].title;
      const description = data.items[randomIndex].description;
      const link = data.items[randomIndex].link;

      // Display the headline and description in the popup
      headlineElement.innerHTML = `<a href="${link}" target="_blank">${headline}</a><br>${description}`;

      // Fetch a random video from the playlist
      await fetchRandomVideo();

    } else {
      headlineElement.innerText = "Could not fetch reading content.";
      videoFrame.src = ''; // Clear video frame if content is not available
    }

  } catch (error) {
    console.error("Error fetching reading content: ", error);
    headlineElement.innerText = "Error loading reading content.";
    videoFrame.src = ''; // Clear video frame on error
  }
}

async function fetchRandomVideo() {
  try {
    const response = await fetch(PLAYLIST_URL);
    const text = await response.text();

    // Use a regex to extract video IDs from the page
    const videoIds = [];
    const videoRegex = /"videoId":"([^"]+)"/g;
    let match;

    while ((match = videoRegex.exec(text)) !== null) {
      videoIds.push(match[1]);
    }

    if (videoIds.length > 0) {
      const randomVideoId = videoIds[Math.floor(Math.random() * videoIds.length)];
      videoFrame.src = `https://www.youtube.com/embed/${randomVideoId}?autoplay=1`;
    } else {
      console.warn("No videos found in the playlist.");
      videoFrame.src = ''; // Clear video frame if no valid videos found
    }
  } catch (error) {
    console.error("Error fetching video content: ", error);
    videoFrame.src = ''; // Clear video frame on error
  }
}

// Add event listener to the button to fetch new content
newContentButton.addEventListener('click', fetchReadingContent);

// Initial fetch for reading content when the popup is opened
fetchReadingContent();


