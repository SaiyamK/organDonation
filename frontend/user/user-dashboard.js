// user-dashboard.js
document.addEventListener('DOMContentLoaded', function () {
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
