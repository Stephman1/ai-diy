document.getElementById("reloadQuiz").addEventListener("click", generateQuiz);

// Load available topics from topics.json
function loadTopics() {
  fetch('questions/topics.json')
    .then(response => response.json())
    .then(data => {
      const topicDropdown = document.getElementById("topic");
      topicDropdown.innerHTML = ''; // Clear existing options
      if (!data.topics || data.topics.length === 0) {
        alert("No topics found in the topics.json file.");
        return;
      }

      // Populate dropdown with topics
      data.topics.forEach(topic => {
        const option = document.createElement("option");
        option.value = topic;
        option.textContent = topic.replace('.json', '').toUpperCase();
        topicDropdown.appendChild(option);
      });
    })
    .catch(error => {
      alert("Could not load topics. Please check the file.");
      console.error(error);
    });
}

// Event listener to generate quiz based on the selected topic
document.getElementById("topic").addEventListener("change", generateQuiz);

function generateQuiz() {
  const selectedTopic = document.getElementById("topic").value;

  if (!selectedTopic) {
    return;  // No topic selected, so do nothing
  }

  fetch(`questions/${selectedTopic}`)
    .then(response => {
      if (!response.ok) {
        throw new Error(`Failed to load ${selectedTopic}`);
      }
      return response.json();
    })
    .then(data => {
      if (!data || !data.questions || data.questions.length === 0) {
        alert("No questions found in the selected topic.");
        return;
      }

      const randomQuestions = getRandomQuestions(data.questions, 2);
      displayQuiz(randomQuestions);
    })
    .catch(error => {
      alert("Could not fetch questions. Please check the file.");
      console.error(error);
    });
}

// Get random questions from the array
function getRandomQuestions(allQuestions, numberOfQuestions) {
  const randomQuestions = [];
  const usedIndexes = new Set();

  while (randomQuestions.length < numberOfQuestions) {
    const randomIndex = Math.floor(Math.random() * allQuestions.length);
    
    if (!usedIndexes.has(randomIndex)) {
      randomQuestions.push(allQuestions[randomIndex]);
      usedIndexes.add(randomIndex);
    }
  }

  return randomQuestions;
}

// Display quiz questions and options
function displayQuiz(questions) {
  const quizContainer = document.getElementById("quizContainer");
  quizContainer.innerHTML = "";  // Clear any previous quiz

  questions.forEach(q => {
    const questionDiv = document.createElement("div");
    questionDiv.classList.add("question");
    questionDiv.innerHTML = `<p>${q.question}</p>`;

    q.answers.forEach((answer, index) => {
      const answerButton = document.createElement("button");
      answerButton.classList.add("option");
      answerButton.innerText = answer;
      answerButton.addEventListener("click", () => checkAnswer(index, q.correctAnswer));
      questionDiv.appendChild(answerButton);
    });

    quizContainer.appendChild(questionDiv);
  });
}

// Check if the selected answer is correct
function checkAnswer(selectedOption, correctAnswer) {
  if (selectedOption === correctAnswer) {
    alert("Correct!");
  } else {
    alert("Incorrect, try again!");
  }
}

// Load topics when the popup is opened
loadTopics();
