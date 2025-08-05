const openBtn = document.getElementById("openPopup");
const popupForm = document.getElementById("popupForm");
const resultPopup = document.getElementById("resultPopup");
const resultText = document.getElementById("resultText");

openBtn.onclick = () => {
  popupForm.classList.remove("hidden");
};

function closePopup() {
  popupForm.classList.add("hidden");
}

function closeResult() {
  resultPopup.classList.add("hidden");
  document.getElementById("userInput").value = "";
}

const descriptions = {
  INTJ: "The Architect: Imaginative, strategic, and analytical.",
  INTP: "The Logician: Innovative inventors with a thirst for knowledge.",
  ENTJ: "The Commander: Bold, imaginative, and strong-willed leaders.",
  ENTP: "The Debater: Smart, curious thinkers who love intellectual challenges.",
  
  INFJ: "The Advocate: Insightful, idealistic, and quietly inspiring.",
  INFP: "The Mediator: Thoughtful, empathetic, and loyal to their values.",
  ENFJ: "The Protagonist: Charismatic leaders, inspiring and empathetic.",
  ENFP: "The Campaigner: Energetic, enthusiastic, and creative free spirits.",
  
  ISTJ: "The Logistician: Responsible, serious, and detail-oriented.",
  ISFJ: "The Defender: Warm protectors who value traditions and loyalty.",
  ESTJ: "The Executive: Practical managers who take charge of projects.",
  ESFJ: "The Consul: Caring, social, and highly attuned to others’ needs.",
  
  ISTP: "The Virtuoso: Bold experimenters and practical problem solvers.",
  ISFP: "The Adventurer: Gentle artists who love exploring beauty.",
  ESTP: "The Entrepreneur: Energetic thrill-seekers who love the spotlight.",
  ESFP: "The Entertainer: Fun-loving, spontaneous, and charming performers."
};

function predict() {
  const userInput = document.getElementById("userInput").value.trim();
  if (!userInput) {
    alert("Please type something!");
    return;
  }

  // Close input popup
  closePopup();

  // Show result popup
  resultPopup.classList.remove("hidden");
  resultText.textContent = "Predicting...";
  document.getElementById("loading").classList.remove("hidden"); // show loading animation

  // Call backend API (Flask)
  fetch("http://127.0.0.1:5000/predict", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text: userInput }),
  })
    .then((res) => res.json())
    .then((data) => {
      const type = data.prediction;
      resultText.innerText = type;
      document.getElementById("resultDesc").innerText = descriptions[type] || "";
    })

    .catch(() => {
      resultText.textContent = "Server error!";
    })
    .finally(() => {
      document.getElementById("loading").classList.add("hidden"); // hide loading in all cases
    });
}

function clearInput() {
  document.getElementById("userInput").value = "";
  document.getElementById("resultText").innerText = "";
  document.getElementById("resultDesc").innerText = "";
  resultPopup.classList.add("hidden");
}
