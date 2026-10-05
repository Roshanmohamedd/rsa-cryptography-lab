let keys = null;

const $ = (id) => document.getElementById(id);

function showSteps(steps) {
  $("steps").innerHTML = steps.map((s, i) => `
    <div class="step">
      <div class="step-num">${String(i + 1).padStart(2, "0")}</div>
      <div>result = ${s.result}, base = ${s.base}, exponent = ${s.exponent}</div>
    </div>
  `).join("");
}

$("generate").addEventListener("click", async () => {
  $("keyError").textContent = "";
  const response = await fetch("/api/generate", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({p: $("p").value, q: $("q").value})
  });
  const data = await response.json();

  if (!response.ok) {
    $("keyResult").classList.add("hidden");
    $("keyError").textContent = data.error;
    return;
  }

  keys = data;
  $("keyResult").classList.remove("hidden");
  $("keyResult").innerHTML = Object.entries(data).map(([key, value]) => `
    <div class="metric"><small>${key}</small><strong>${value}</strong></div>
  `).join("");
});

$("encrypt").addEventListener("click", async () => {
  if (!keys) {
    $("encryptResult").innerHTML = '<div class="error">Generate keys first.</div>';
    return;
  }

  const response = await fetch("/api/encrypt", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({
      message: $("message").value,
      e: keys.e,
      n: keys.n
    })
  });
  const data = await response.json();

  if (!response.ok) {
    $("encryptResult").innerHTML = `<div class="error">${data.error}</div>`;
    return;
  }

  $("ciphertext").value = data.ciphertext;
  $("encryptResult").innerHTML =
    `<div class="output">ciphertext = ${data.ciphertext}</div>`;
  showSteps(data.steps);
});

$("decrypt").addEventListener("click", async () => {
  if (!keys) {
    $("decryptResult").innerHTML = '<div class="error">Generate keys first.</div>';
    return;
  }

  const response = await fetch("/api/decrypt", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({
      ciphertext: $("ciphertext").value,
      d: keys.d,
      n: keys.n
    })
  });
  const data = await response.json();

  if (!response.ok) {
    $("decryptResult").innerHTML = `<div class="error">${data.error}</div>`;
    return;
  }

  $("decryptResult").innerHTML =
    `<div class="output">original message = ${data.message}</div>`;
  showSteps(data.steps);
});
