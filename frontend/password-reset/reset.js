// const showAlert = (message) => {
//     window.alert(message);
// };

// const validatePassword = (password) => {
// return ;
// };

// const validateEmail = (email) => {
// return ;
// };

// const validateOTP = (otp) => {
//     return otp !== '';
// };

// const changePassword = async () => {
// const email = document.getElementById("email").value.trim();
// const otp = document.getElementById("otp").value.trim();
// const password = document.getElementById("password").value.trim() + '';
document.getElementById("btn-change").addEventListener("click", async (e) => {
    e.preventDefault();
    try {
        const email = document.getElementById("email").value.trim();
        const otp = document.getElementById("otp").value.trim();
        const password = document.getElementById("password").value.trim() + '';

        if (!password && (password.length < 8 || !password.split('').some(c => c.match(/^[0-9A-Z]$/)))) {
            alert("Please enter a strong password 8 characters long having a digit or an uppercase letter.");
        } else if (!email.match(/^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/)) {
            alert("Please enter a valid email!");
        } else if (!otp) {
            alert("OTP can not be empty!");
        } else {
            try {
                const { data, status } = await axios.put(`http://localhost:8000/changePassword?email=${email}&old_password=${otp}&new_password=${password}`)//, { validateStatus: (s) => [200, 404, 401].includes(s) });
                if (status === 200) {
                    await swal("Good job!", "You clicked the button!", "success", {
                        button: "Aww yiss!",
                    });
                    location.href = "../user/login.html";
                } else if (status === 404) {
                    alert("Provided email is not associated with any account!");
                } else if (status === 401) {
                    alert("Invalid OTP/Temporary password");
                }
            } catch (err) {
                console.log(err);
                alert("Something went wrong!");
            }
        }
    } catch (err) {
        console.log(err);
    }
});