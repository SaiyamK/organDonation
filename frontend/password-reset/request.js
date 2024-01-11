const fetchOTP = async () => {
	try {
		const email = document.getElementById("email").value.trim();
		const { data, status } = await axios.put(`http://localhost:8000/forgotPassword?email=${email}`, {}, { validateStatus: (s) => s === 200 || s === 404 });
		if (status === 200) {
			window.alert(`Here's your temporary password, please use it to reset your password: ${data.temporaryPassword}`);
			window.location = "/modules/admin/reset.html";
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
	await fetchOTP();
});