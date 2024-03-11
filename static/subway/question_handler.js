// Event listener for button click
document
  .getElementById("button-addon2")
  .addEventListener("click", function (event) {
    event.preventDefault();
    handleQuestionAPIRequest();
  });

// Event listener for Enter key press in the input field
document
  .getElementById("questionInput")
  .addEventListener("keyup", function (event) {
    if (event.key === "Enter") {
      handleQuestionAPIRequest();
    }
  });
var makingRequest = false;
function handleQuestionAPIRequest() {
  // Get the user's question
  const question = document.getElementById("questionInput").value;
  if (question.length < 10) {
    document.getElementById("answerContent").innerHTML =
      "Do type full question so AI can understand.";
    return;
  }
  // Prevent multiple API call
  if (makingRequest) {
    return;
  }

  document.getElementById("loadingSpinner").style.display = "inline-block";
  document.getElementById("answerContent").innerHTML = "";

  // Make an API request to get the answer
  makingRequest = true;
  axios
    .get("/ask", { params: { question: question } })
    .then((response) => {
      makingRequest = false;
      document.getElementById("loadingSpinner").style.display = "none";

      const answer = response.data.answer;
      // Display the answer
      document.getElementById("answerContent").innerHTML = `<p>${answer}</p>`;
    })
    .catch((error) => {
      makingRequest = false;
      document.getElementById("loadingSpinner").style.display = "none";
      // Display the answer
      document.getElementById("answerContent").innerHTML = `<p>Some error occur when making request</p>`;
      console.error("Error fetching answer:", error);
    });
}
