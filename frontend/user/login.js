
async function validatePassword() {
  var password = document.getElementById('password').value;
  var email = document.getElementById('Email').value;

  if (!/^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/.test(email) || email.trim() === "")
    document.getElementById('errorMessage').innerText = 'Enter valid email!';
  else {

    document.getElementById('spinner').classList.toggle('d-none');
    try {
      const response = await axios.post(`http://127.0.0.1:8000/authenticateUser?email=${email}&password=${password}`);
      console.log('Response from server:', response.data);
      const token = response.data.token;
      sessionStorage.setItem('authToken', token);
      alert("Logged in!");
      window.location.href = 'user-dashboard.html';
    } catch (err) {
      console.error('Error:', err);
      window.alert('Some error occurred')
    } finally {
      document.getElementById('spinner').classList.toggle('d-none');
    }
  }
}