document.addEventListener("DOMContentLoaded", () => {
  const num1 = document.getElementById("num1");
  const num2 = document.getElementById("num2");
  const opSelect = document.getElementById("op");
  const resultValue = document.getElementById("result-value");
  const calcBtn = document.getElementById("calc");
  const clearBtn = document.getElementById("clear");

  // click on operator buttons sets the select and calculates
  document.querySelectorAll(".op-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      opSelect.value = btn.dataset.op;
      doCalculate();
    });
  });

  calcBtn.addEventListener("click", doCalculate);
  clearBtn.addEventListener("click", () => {
    num1.value = "";
    num2.value = "";
    resultValue.textContent = "";
    num1.focus();
  });

  function showMessage(msg) {
    resultValue.textContent = msg;
  }

  function doCalculate() {
    const n1 = num1.value.trim();
    const n2 = num2.value.trim();
    const op = opSelect.value;

    if (n1 === "" || n2 === "") {
      showMessage("Please enter both numbers.");
      return;
    }

    fetch("/api/calc", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ num1: n1, num2: n2, op: op })
    })
      .then(async res => {
        const body = await res.json().catch(() => ({}));
        if (res.ok && body.result !== undefined) {
          showMessage(body.result);
        } else {
          showMessage(body.error || "Error calculating.");
        }
      })
      .catch(() => {
        showMessage("Network or server error.");
      });
  }

  // Keyboard support
  [num1, num2].forEach(inp => {
    inp.addEventListener("keydown", (e) => {
      if (e.key === "Enter") {
        doCalculate();
      } else if (["+", "-", "*", "/"].includes(e.key)) {
        opSelect.value = e.key;
        // small debounce to allow keypress to finish
        setTimeout(doCalculate, 10);
      }
    });
  });
});
