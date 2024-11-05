# FAQs

`AI DIY Episode 1: Creating a French Language Learning Browser Extension with ChatGPT` is available on [YouTube](https://youtu.be/S96Mbqo6fu8?si=GHxNkybAlTEjlQfJ).

## What did you build in this episode?

A Chrome browser extension that helps me to learn French when I am browsing the web. Each time I load the extension it connects to a News article from the Le Monde website and a French-language YouTube video from a playlist.

![French Practice Chrome extension](https://github.com/user-attachments/assets/a5c3cf56-4abb-486b-9f9b-4217ce1f0e34)

## Can I build the Chrome extension with the code in this folder?

Yes, if you upload this folder (exclude this README file) into Chrome browser the French learning extension should work as shown in the [video](https://youtu.be/S96Mbqo6fu8?si=K_c-Xuei_ljMcIiI&t=436).

## What YouTube playlist should I use?

The code as is links to the following YouTube playlist, [French Culture & Society](https://www.youtube.com/playlist?list=PLmK-vbXTxuypeIF5rXp_MlI9SkXcNQacV). Substitute in another playlist ID into the popup.js file if needed. I would suggest that you ask ChatGPT to connect to your own pre-existing playlist (give the exact URL) and remember to set the playlist to `unlisted` or `public`. I would also tell ChatGPT how many videos are in the playlist.

![YouTube playlist ID in the URL](https://github.com/user-attachments/assets/3560b4be-297b-4305-b1a6-cd48b18ded65)

<img width="817" alt="YouTube playlist ID in popup.js" src="https://github.com/user-attachments/assets/f5d7f5da-5bf2-4b51-8a2b-2c16ea022cce">

<img width="817" alt="Set total videos in popup.js" src="https://github.com/user-attachments/assets/4cd5ddba-3c1c-4074-aaa3-3d65f885f1bb">

## What text or prompt did you enter into ChatGPT to retrieve the code?

The first prompt that I entered was: 

`I want a Chrome browser extension that will help me to learn French when I am browsing the web. I want to practice reading and listening in French. I want to practice reading by reading the News, therefore I want to get a snippet from an online News article from the Le Monde website. I also want to practice listening in French, therefore I want the extension to link to a YouTube playlist that contains French listening videos. I want to be able to watch the video and read the news snippet in the extension. Can you give me the code to be able to build this extension?`

## Do you pay for ChatGPT?

No, I only used the free version of ChatGPT to make the French learning extension.

## How do I create the HTML, JavaScript, Manifest and CSS files?

I copied and pasted the relevant code given by ChatGPT into four files on my local computer named `popup.html`, `popup.js`, `manifest.json` and `styles.css`. You can use a standard text editor like Notepad (pre-installed on Windows) or TextEdit (pre-installed on Mac) and save the file as `popup.html` or `popup.js`. You do not need any other application to create HTML and JavaScript files.

## Do I have to use Chrome?

I use the Chrome browser for accessing the web. Please tell ChatGPT if you want to build the extension for another browser that you use.

## Do I have to use ChatGPT as my Generative AI assistant?

Not necessarily, I am thinking of using Gemini for other episodes of AI DIY.

## URLs used in the episode

Connect to Le Monde News through a [RSS feed](https://www.lemonde.fr/actualite-medias/article/2019/08/12/les-flux-rss-du-monde-fr_5498778_3236.html): https://api.rss2json.com/v1/api.json?rss_url=https://www.lemonde.fr/rss/une.xml

Connect to a YouTube playlist: https://www.youtube.com/playlist?list=PLmK-vbXTxuypeIF5rXp_MlI9SkXcNQacV
