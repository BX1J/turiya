const form = document.getElementById("downloadForm");
const urlInput = document.getElementById("urlInput");
const modeSelect = document.getElementById("modeSelect"); // Unused Yet
const qualitySelect = document.getElementById("qualitySelect"); // Unused Yet
const downloadBtn = document.getElementById("downloadBtn");

form.addEventListener("submit", (e) => {
  e.preventDefault();
  let link = JSON.stringify({"link":urlInput.value});
  fetch('/api/download',{'method':"POST","body":link,headers: {"Content-Type": "application/json"}})
  .then(response=>response.json())
  .then(data=>console.log(data))
  .catch(err=>console.log(err))
});
