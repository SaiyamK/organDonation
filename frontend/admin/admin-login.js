const validateEntries = async (username, password) => new Promise((res, rej) => {
    setTimeout(() => {
        if (username === 'admin' && password === '123') res({
            message: "Logged in successfully!",
            status: 200,
            next: 'admin-dashboard.html'
        })
        else rej({
            message: "Incorrect username or password!",
            status: 401,
            next: null
        })
    }, 2000);
});

document.getElementById('btn-login').addEventListener("click", async (e) => {
    e.preventDefault();
    const username = document.getElementById("username").value.trim().replaceAll(' ', '');
    const password = document.getElementById("password").value;
    const spinner = document.getElementById("spinner");
    spinner.classList.toggle("d-none");
    try {
        const res = await validateEntries(username, password);
        window.alert(res.message);
        window.location = res.next;
    } catch (err) {
        console.log(err.message);
    } finally {
        spinner.classList.toggle("d-none");
    }
});