var data = [];

function updateResults() {
  // Clear the current list
  resultList.innerHTML = "";

  // Get the search query
  const query = searchInput.value.toLowerCase();
  cleanMap();
  // Filter the data based on the query
  axios
    .get("api/subway/", { params: { search: query } })
    .then(function (response) {
      // Handle the successful response
      data = response.data;
      populateDataToHtml(response.data);
    })
    .catch(function (error) {
      // Handle errors
      console.error("Error fetching data:", error);
    });

  // Populate the result list with the filtered results
}

function populateDataToHtml(data) {
  data.forEach((result) => {
    const listItem = document.createElement("div");
    listItem.className = "list-group-item list-group-item-action";
    listItem.onclick = function () {
      showCurrentMarker(result.lat, result.long);
    };
    listItem.innerHTML =
      "<h4>" +
      result.name +
      "</h4><div><p>" +
      result.address +
      "</p><p></p><p>" +
      result.operating_time +
      "</p><p></p></div>";
    resultList.appendChild(listItem);
  });
}

document.addEventListener("DOMContentLoaded", function () {
  // Get references to the search input and result list
  const searchInput = document.getElementById("searchInput");

  searchInput.addEventListener("keypress", function (event) {
    // Check if the pressed key is Enter (key code 13)
    if (event.key === "Enter") {
      // Call your search function or API call here
      updateResults();
    }
  });
  // Initial update when the page loads
  updateResults();
});
