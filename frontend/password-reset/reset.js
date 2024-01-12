const changePassword = async () => {
    const email = document.getElementById("email").value.trim();
    const otp = document.getElementById("otp").value.trim();
    const password = document.getElementById("password").value.trim() + '';
    if (password && (password.length < 8 || !password.split('').some(c => c.match(/^[0-9A-Z]$/)))) {
        window.alert("Please enter a strong password 8 characters long having a digit or an uppercase letter.")
    } else if (!email.match(/^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/)) {
        window.alert("Please enter a valid email!");
    } else if (!otp) {
        window.alert("OTP can not be empty!");
    } else {
        try {
            const { data, status } = await axios.put(`http://localhost:8000/changePassword?email=${email}&old_password=${otp}&new_password=${password}`, {}, { validateStatus: (s) => [200, 404, 401].includes(s) });
            if (status === 200) {
                window.alert("Password changed successfully!");
                const chunks = window.location.pathname.split('/');
                chunks.splice(chunks.length - 1);
                chunks.push('admin-login.html');
                console.log(chunks.join('/'));
                window.location = chunks.join('/');
            } else if (status === 404) {
                window.alert("Provided email is not associated with any account!")
            } else if (status === 401) {
                window.alert("Invalid OTP/Temporary password");
            }
        } catch (err) {
            window.alert("Something went wrong!");
        }
    }
};

document.getElementById("btn-change").addEventListener("click", async (e) => {
    e.preventDefault();
    const spinner = document.getElementById("spinner");
    spinner.classList.toggle("d-none");
    try {
        await changePassword();
    }
    catch (err) {
        window.alert("Something went wrong!");
        console.log(err);
    }
    finally {
        spinner.classList.toggle("d-none");
    }
});