// user-dashboard.js
let FirstName;
let LastName;
let email;
let mobile;
let address;
let bloodgroup;
let hospitalid;
let statusPerson;
let hdata;
const authToken = +sessionStorage.getItem('authToken');
const contribTable = document.getElementById("contrib-table");


if (!authToken || isNaN(authToken)) window.location = "login.html";
async function getHospitalsDetails() {
    const response = await axios.get("http://127.0.0.1:8000/getHospital");
    hdata = response.data;
    console.log(typeof (hdata));
}
getHospitalsDetails();

async function userDetails() {

    if (authToken) {
        try {
            const id = authToken;
            console.log(id)
            const response = await axios.get(`http://127.0.0.1:8000/getUsersByTokenId?user_id=${id}`);
            console.log(response);
            FirstName = response.data.first_name;
            LastName = response.data.last_name;
            email = response.data.email;
            mobile = response.data.mobile;
            address = response.data.address;
            bloodgroup = response.data.bloodGroup;
            const hid = response.data.hospital_id;
            const hospitalname = hdata[hid - 1].hospital_name;
            if (response.data.isAlive) {
                statusPerson = "Alive"
            }
            else {
                statusPerson = "Dead"
            }
            const container = document.getElementById("profile-section");
            container.innerHTML = `<p id="First-Name"><strong>First Name:</strong> ${FirstName}</p><p id="Last-Name"><strong>Last Name:</strong> ${LastName}</p>  <p id="Email"><strong>Email:</strong> ${email}</p><p id="Mobile"><strong>Mobile:</strong> ${mobile}</p><p id="Address"><strong>Address:</strong> ${address}</p><p id="Blood-Group"><strong>Blood Group:</strong> ${bloodgroup}</p><p id="Hospital-id"><strong>Hospital Name:</strong> ${hospitalname}</p><p id="Status"><strong>Status:</strong> ${statusPerson}</p>`
        }
        catch (err) {
            console.log(err);
        }
    }
}
document.addEventListener('DOMContentLoaded', function () {

    userDetails();
    console.log(FirstName);

    // Get all tab links and tab content elements
    const tabLinks = document.querySelectorAll('.nav-tabs .nav-link');
    // const tabContents = document.querySelectorAll('.tab-content .tab-pane');
    const tabContents = document.querySelectorAll('.tab-content');

    console.log(tabLinks, tabContents);

    // Add click event listeners to the tab links
    tabLinks.forEach(function (tabLink) {
        tabLink.addEventListener('click', function (event) {
            event.preventDefault();

            // Remove 'active' class from all tab links
            tabLinks.forEach(function (link) {
                link.classList.remove('active');
            });

            // Add 'active' class to the clicked tab link
            this.classList.add('active');

            // Hide all tab contents
            tabContents.forEach(function (content) {
                content.classList.add('d-none');
            });

            // Show the corresponding tab content based on the clicked link
            const tabId = this.getAttribute('href').substring(1);
            const selectedTabContent = document.getElementById(tabId);

            // Toggle the 'd-none' class to display/hide the tab content
            selectedTabContent.classList.toggle('d-none');
        });
    });
});

function logout() {
    sessionStorage.clear();
    window.location = "index.html";
    console.log('Successfully logged out')

}

//CONTRIBUTE SECTION

const fetchPrevContributions = async () => {
    try {
        const res = await axios.get(`http://localhost:8000/previousContributions/${authToken}`);
        res.data.forEach(contrib => {
            contribTable.innerHTML += `
                <tr>
                    <td>${contrib.organ_name}</td>
                    <td>${contrib.recipient_name !== null ? contrib.recipient_name : 'Awaiting recipient'}</td>
                    <td>${contrib.donation_status}</td>
                </tr>
            `;
        });
    } catch (err) {
        console.log(err);
    }
}
fetchPrevContributions();

const makeDonation = async (e) => {
    e.preventDefault();
    const contribSpinner = document.getElementById("contrib-spinner");
    try {
        const organId = +document.getElementById("organSelect").value;
        const consent = document.getElementById("consentCheckbox").checked;
        contribSpinner.classList.toggle("d-none");
        if (!consent) window.alert("Please provide your consent by checking the box.");
        else {
            const res = await axios.put(`http://localhost:8000/contribute/${authToken}/${organId}`);
            // window.alert(res.data.message);
            await swal("", "Thanks for your contribution", "success", {
                button: "OK",
            });
            window.location.reload();
        }
    } catch (err) {
        window.alert("Something went wrong!");
    } finally {
        contribSpinner.classList.toggle("d-none");
    }
}
document.getElementById("btn-contrib").addEventListener("click", makeDonation);

//REQUESTS

const getPrevRequests = async () => {
    const tbReq = document.getElementById("tb-req")
    try {
        const res = await axios.get(`http://localhost:8000/previousRequests/${authToken}`);
        res.data.forEach(contrib => {
            tbReq.innerHTML += `
                <tr>
                    <td>${contrib.organ_name}</td>
                    <td>${contrib.donor_name !== null ? contrib.donor_name : 'Awaiting donor'}</td>
                    <td>${contrib.donation_status}</td>
                </tr>
            `;
        });
    } catch (err) {
        console.log(err);
    }
}
getPrevRequests();

document.getElementById("btn-req").addEventListener("click", async (e) => {
    e.preventDefault();
    const reqSpinner = document.getElementById("req-spinner");
    try {
        const organId = +document.getElementById("organRequestSelect").value;
        const reason = document.getElementById("reasonTextarea").value;
        console.log(authToken, organId, reason);
        reqSpinner.classList.toggle("d-none");
        if (!reason) window.alert("Please provide a reason for your request.");
        else {
            const res = await axios.put(`http://localhost:8000/request/${authToken}/${organId}?reason=${reason}`);
            // window.alert(res.data.message);
            await swal("", "Request registered", "success", {
                button: "OK",
            });
            location.reload();
        }
    } catch (err) {
        window.alert("Something went wrong!")
    } finally {
        reqSpinner.classList.toggle("d-none");
    }
});

document.getElementById("logout").addEventListener("click", (e) => {
    e.preventDefault();
    sessionStorage.removeItem(authToken);
    window.location = "login.html";
});