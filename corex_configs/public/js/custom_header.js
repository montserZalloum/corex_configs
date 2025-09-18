// // Custom Header Navigation for Frappe ERPNext
// // This script adds page-dependent navigation links to the header

$(document).ready(function() {
    // Try multiple times to ensure DOM is ready
    // initializeWithRetry();
    setLandingPageLink__LogoHeader();
});

function setLandingPageLink__LogoHeader() {
    if (document.querySelector('.navbar-brand.navbar-home')) {
        document.querySelector('.navbar-brand.navbar-home').setAttribute('href', '/landing');
    }
}