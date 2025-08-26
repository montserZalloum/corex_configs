$(document).on('login_rendered', function() {
    // Ensure this patch is only applied when the login handlers are available
    if (window.login && login.login_handlers && login.login_handlers[200]) {
        // Store the original login handler so we can use it as a fallback
        const original_handler = login.login_handlers[200];
        // Overwrite the handler with our custom version
        login.login_handlers[200] = function(data) {
            // If the login is successful AND our custom redirect is present...
            if (data.message === 'Logged In' && data.redirect_to) {
                // Use our custom redirect logic
                login.set_status('Success', 'green'); 
                // document.body.innerHTML = '<div style="display: flex; justify-content: center; align-items: center; height: 100vh;"><h1>Loading...</h1></div>';
                window.location.href = frappe.utils.sanitise_redirect(data.redirect_to);

            } else {
                // Otherwise, execute the original handler for all other cases
                original_handler.call(this, data);
            }
        };
    }
}); 