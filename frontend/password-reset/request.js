const fetchOTP = async () => {
	try {
		const email = document.getElementById("email").value.trim();
		const { data, status } = await axios.put(`http://localhost:8000/forgotPassword?email=${email}`, {}, { validateStatus: (s) => s === 200 || s === 404 });
		if (status === 200) {
			window.location = "reset.html";
		} else if (status === 404) {
			window.alert(`No account exists for this email!`);
		}
	} catch (err) {
		console.log(err);
		window.alert("Something went wrong!");
	}
}

document.getElementById('btn-otp').addEventListener("click", async (e) => {
	e.preventDefault();
	document.getElementById("spinner").classList.toggle('d-none');
	await fetchOTP();
	document.getElementById("spinner").classList.toggle('d-none');
});