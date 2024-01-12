const validateEntries = async (username, password) => {
    try {
        const res = await axios.post(`http://localhost:8000/authenticateUser?email=${username}&password=${password}`);
        console.log(res);
    } catch (err) {
        if (err.response.status === 404) {
            await swal("Unauthorized", "Invalid credentials", "error", {
                button: "Close",
            });
        }
        throw err;
    }
};



document.getElementById('btn-login').addEventListener("click", async (e) => {
    e.preventDefault();
    const username = document.getElementById("username").value.trim().replaceAll(' ', '');
    const password = document.getElementById("password").value;
    const spinner = document.getElementById("spinner");
    spinner.classList.toggle("d-none");
    try {
        await validateEntries(username, password);
        await swal("Welcome", "Admin verified!", "success", {
            button: "Dashboard",
        });
        window.location = "admin-dashboard.html";
    } catch (err) {
        console.log(err.message);
    } finally {
        spinner.classList.toggle("d-none");
    }
});