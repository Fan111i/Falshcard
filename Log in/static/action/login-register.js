function signin() {
  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;

  if (!username || !password) {
    alert("Please input value");
    return;
  }
  fetch("/login", {
    method: 'POST',
    body: JSON.stringify({
      username, password
    })
  })
    .then(res => res.json())
    .then(res => {
      alert("Login success")
    })
}

function signup() {
  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;
  const confirmPassword = document.getElementById("confirm-password").value;
  if (!username || !password || !confirmPassword) {
    alert("Please input value");
    return;
  }
  if (password !== confirmPassword) {
    alert("Password and confirm password not match");
    return;
  }
  fetch("/login", {
    method: 'POST',
    body: JSON.stringify({
      username, password, confirmPassword
    })
  })
    .then(res => res.json())
    .then(res => {
      alert("Login success")
    })
}