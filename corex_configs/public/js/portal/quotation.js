// my_app/my_app/public/js/quotation.js
$(document).ready(function() {
    // Only run on portal pages for /quotations
    if (window.location.pathname.includes('/quotations')) {
        console.log('Running in portal on /quotations');
        // Create button
        var button = $('<button class="btn btn-primary">New Request-a-Quote</button>');
        button.click(function() {
            window.location.href = '/request-a-quote/new';
        });
        // Append to web form actions or another container
        $('.page-header-actions-block').prepend(button); // Adjust selector as needed
    }
});