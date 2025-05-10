async function uploadCSV() {
  const fileInput = document.getElementById("csvFile");
  const generateButton = document.getElementById("generateButton");
  const loadingSpinner = document.getElementById("loading");
  const resultDiv = document.getElementById("results");

  const file = fileInput.files[0];
  if (!file) {
    alert("Please select a CSV file.");
    return;
  }

  // Disable the generate button and show loading spinner
  generateButton.disabled = true;
  loadingSpinner.style.display = "block";

  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch("http://127.0.0.1:5000/upload_csv", {
    method: "POST",
    body: formData,
  });

  resultDiv.innerHTML = "";
  loadingSpinner.style.display = "none"; // Hide the spinner when done
  generateButton.disabled = false; // Enable the button again

  if (response.ok) {
    const summaries = await response.json();
    summaries.forEach((summary) => {
      const div = document.createElement("div");
      div.className = "summary";
      div.innerHTML = `
        <strong>${summary["Employee Name"]} (${summary["Employee ID"]})</strong><br>
        ${summary["Summary"]}
      `;
      resultDiv.appendChild(div);
    });
  } else {
    const error = await response.json();
    resultDiv.innerHTML = `<p style="color:red;">Error: ${error.error}</p>`;
  }
}
