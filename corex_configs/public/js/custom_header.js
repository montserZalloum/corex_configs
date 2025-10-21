$(document).ready(function() {
    setLandingPageLink__LogoHeader();
    addBackButton();
});

function setLandingPageLink__LogoHeader() {
    if (document.querySelector('.navbar-brand.navbar-home')) {
        document.querySelector('.navbar-brand.navbar-home').setAttribute('href', '/app/landing');
    }
}

function addBackButton() {
    // Wait for the page to be fully loaded and DOM elements to be available
    setTimeout(function() {
        addBackButtonToPageTitle();
    }, 100);
    
    // Also add back button when navigating between pages
    $(document).on('page-change', function() {
        setTimeout(function() {
            addBackButtonToPageTitle();
        }, 100);
    });
    
    // Monitor for dynamic content changes (for modals, dialogs, etc.)
    const observer = new MutationObserver(function(mutations) {
        let shouldAddButton = false;
        mutations.forEach(function(mutation) {
            if (mutation.type === 'childList' && mutation.addedNodes.length > 0) {
                // Check if any added nodes contain page-title elements
                mutation.addedNodes.forEach(function(node) {
                    if (node.nodeType === 1) { // Element node
                        if (node.querySelector && (node.querySelector('.page-head .page-title') || node.matches('.page-head .page-title'))) {
                            shouldAddButton = true;
                        }
                    }
                });
            }
        });
        
        if (shouldAddButton) {
            setTimeout(function() {
                addBackButtonToPageTitle();
            }, 50);
        }
    });
    
    // Start observing
    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
}

function addBackButtonToPageTitle() {
    // Find all page title containers that might exist
    const pageTitles = document.querySelectorAll('.page-head .page-title');
    
    // Process each page title container
    pageTitles.forEach(function(pageTitle) {
        // Check if back button already exists in this container
        if (pageTitle.querySelector('.custom-back-btn')) return;
        
        // Find the sidebar toggle button in this container
        const sidebarToggle = pageTitle.querySelector('.sidebar-toggle-btn');
        if (!sidebarToggle) return;
        
        // Create back button element
        const backButton = createBackButton();
        
        // Insert the back button after the sidebar toggle button
        sidebarToggle.parentNode.insertBefore(backButton, sidebarToggle.nextSibling);
    });
}

function createBackButton() {
    const backButton = document.createElement('button');
    backButton.className = 'btn-reset custom-back-btn custom-back-btn-in-header';
    backButton.setAttribute('title', 'Go Back');
    backButton.setAttribute('aria-label', 'Go Back');
    // Create the back arrow SVG
    backButton.innerHTML = `
        <svg class="icon icon-sm" >
            <use href="#icon-arrow-left"></use>
        </svg>
    `;
    
    // Add click functionality to go back
    backButton.addEventListener('click', function(e) {
        e.preventDefault();
        e.stopPropagation();
        
        // Check if there's history to go back to
        if (window.history.length > 1) {
            window.history.back();
        } else {
            // If no history, redirect to home/dashboard
            window.location.href = '/app/landing';
        }
    });
    
    return backButton;
}

