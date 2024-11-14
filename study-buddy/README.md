# FAQs

There is a short that introduces the `AI DIY Study Buddy` on [YouTube](https://youtube.com/shorts/S94Z-v9qBUI?si=oWphAUr5WcrV5YE3).

<img src="https://github.com/user-attachments/assets/1e19b816-70c3-4463-b986-ef1deeacd57f" width="50%" alt="Study Buddy Chrome extension in use">

## How do I use the Study Buddy?

1. Load the Code into Chrome:
   * Open Chrome and go to the address bar.
   * Type chrome://extensions/ and press Enter.
   * Toggle the "Developer mode" switch at the top right corner.
   * Click the "Load unpacked" button.
   * Navigate to the directory where your extension's source code is located.
   * Select the root directory of your extension and click "Select Folder".

## How do I update the questions and add new topics?

1. Update Questions
   * Go to an existing questions file in the `questions` folder (e.g., `load_balancing.json`) and copy and paste in more or replace the questions in the file.
   * Remember to use the existing format for any new questions.

<img width="50%" alt="Load balancing questions" src="https://github.com/user-attachments/assets/51856192-86a2-41bd-b8e1-f039b02d6b1d">

2. Add a New Topic
   * Create a new topic file, e.g., copy and paste a Wikipedia page into ChatGPT, and ensure the questions are in the same format as the ones in existing files.
   * Place the new topic file in the `questions` folder.
   * You also need to update the `topics.json` with the name of the new file, e.g., `italian.json`.

<img width="308" alt="Update topics file with the name of the new questions file" src="https://github.com/user-attachments/assets/7f86373a-332c-4b60-83a6-e259c088bc28">

3. In both cases, you will also need to visit chrome://extensions/ and update the extensions' code by clicking the `Update` button:

<img src="https://github.com/user-attachments/assets/ec700ca5-d056-417d-826c-b6b16dbd5b65" alt="Update extensions" width="50%">
