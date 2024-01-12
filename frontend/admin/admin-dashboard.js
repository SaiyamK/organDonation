// admin-dashboard.js
/*
<tr>
    <td>1</td>
    <td>User 1</td>
    <td>Kidney</td>
    <td>
        <button class="btn btn-success">Approve</button>
        <button class="btn btn-danger">Reject</button>
    </td>
</tr>
*/
const requestsTable = document.getElementById("requests-table");
const organsTable = document.getElementById("organs-table");

const approveDonation = async (donorId, recipientId, organId, i) => {
    try {
        const res = await axios.put(`http://localhost:8000/approveRequest/${recipientId}/${donorId}/${organId}`);
        window.alert(res.data.message);
        requestsTable.children[i].remove();
    } catch (err) {
        window.alert("Something went wrong");
        console.log(err);
    }
}
const rejectDonation = async (donation_donor_table_id, i) => {
    try {
        const res = await axios.put(`http://localhost:8000/rejectRequest/${donation_donor_table_id}`);
        window.alert(res.data.message);
        requestsTable.children[i].remove();
    } catch (err) {
        window.alert("Something went wrong");
        console.log(err);
    }
}

const deleteDonation = async (donation_id, i) => {
    try {
        const res = await axios.delete(`http://localhost:8000/delete/${donation_id}`);
        window.alert(res.data.message);
        organsTable.children[i].remove();
    } catch (err) {
        window.alert("Something went wrong");
        console.log(err);
    }
}
const fetchPendingRequests = async () => {
    try {
        const res = await axios.get`http://localhost:8000/getRequests`;
        res.data.forEach((req, i) => {
            console.log(req.donation_donor_table_id);
            requestsTable.innerHTML += `
            <tr>
                <td>${i + 1}</td>
                <td>${req.donor_name} - ${req.donation_donor_table_id}</td>
                <td>${req.organ_name}</td>
                <td>${req.recipient_name} - ${req.donation_recipient_table_id}</td>
                <td>
                    <button class="btn btn-success" onclick="approveDonation(${req.donation_donor_table_id}, ${req.donation_recipient_table_id}, ${req.organ_id}, ${i})">Approve</button>
                    <button class="btn btn-danger" onclick="rejectDonation(${req.donation_donor_table_id}, ${i})">Reject</button>
                </td>
            </tr>
            `;
        });
    } catch (err) {
        console.log(err);
    }
}
const fetchAvailableOrgans = async () => {
    try {
        const res = await axios.get`http://localhost:8000/getAvailableOrgansForDonation`;
        res.data.forEach((req, i) => {
            console.log(req.donation_id);
            organsTable.innerHTML += `
            <tr>
                <td>${i + 1}</td>
                <td>${req.organ_name}</td>
                <td>${req.donor_name} - ${req.donor_id}</td>
                <td>
                    <button class="btn btn-danger" onclick="deleteDonation(${req.donation_id}, ${i})">Decline</button>
                </td>
            </tr>
            `;
        });
    } catch (err) {
        console.log(err);
    }
}

fetchPendingRequests();
fetchAvailableOrgans();

document.addEventListener('DOMContentLoaded', function () {
    // Get all tab links and tab content elements
    const tabLinks = document.querySelectorAll('.nav-tabs .nav-link');
    const tabContents = document.querySelectorAll('.tab-content');

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
                content.style.display = 'none';
            });

            // Show the corresponding tab content based on the clicked link
            const tabId = this.getAttribute('href').substring(1);
            const selectedTabContent = document.getElementById(tabId);
            selectedTabContent.style.display = 'block';
        });
    });
});
