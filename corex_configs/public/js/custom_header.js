// // Custom Header Navigation for Frappe ERPNext
// // This script adds page-dependent navigation links to the header

$(document).ready(function() {
    // Try multiple times to ensure DOM is ready
    // initializeWithRetry();
    setLandingPageLink__LogoHeader();
});

// // Listen for route changes
// frappe.router.on('change', function() {
//     setTimeout(function() {
//         initializeWithRetry();
//     }, 500);
// });

// function initializeWithRetry() {
//     var attempts = 0;
//     var maxAttempts = 5;
    
//     function tryInitialize() {
//         attempts++;
//         console.log('Attempt', attempts, 'to initialize custom header');
        
//         if (attempts >= maxAttempts) {
//             console.log('Max attempts reached, giving up');
//             return;
//         }
        
//         // Check if navbar is ready
//         var $navbar = $('.navbar-nav');
//         var $helpDropdown = $('.dropdown-help');
        
//         if ($navbar.length && $helpDropdown.length) {
//             console.log('DOM ready, initializing custom header');
//             initializeCustomHeader();
//         } else {
//             console.log('DOM not ready, retrying in 500ms');
//             setTimeout(tryInitialize, 500);
//         }
//     }
    
//     tryInitialize();
// }

// function initializeCustomHeader() {
//     // Remove any existing custom buttons to avoid duplicates
//     $('.custom-shortcuts-button').remove();
    
//     // Check if we're on a CRM page and add shortcuts if needed
//     var currentRoute = frappe.get_route();
//     console.log('Current route:', currentRoute);
    
//     // Fallback: also check the URL path directly
//     var currentPath = window.location.pathname;
//     console.log('Current path:', currentPath);
    
//     if (isCRMPage(currentRoute) || isCRMPageFromPath(currentPath)) {
//         console.log('CRM page detected, adding shortcuts');
//         addCustomShortcutsButton(currentRoute);
//     } else {
//         console.log('Not a CRM page, shortcuts not shown');
//     }
// }

// function isCRMPage(route) {
//     // Define the CRM pages where shortcuts should be shown
//     var crmPages = [
//         'lead',
//         'opportunity', 
//         'customer',
//         'contact',
//         'appointment'
//     ];
    
//     console.log('Checking route:', route, 'against CRM pages:', crmPages);
    
//     // Check if current route matches any of the CRM pages
//     if (route && route.length > 1) {
//         // In Frappe routes, the doctype name is usually in the second position
//         // e.g., ['List', 'Opportunity', 'List'] -> 'Opportunity'
//         var currentPage = route[1];
//         console.log('Current page:', currentPage);
        
//         // Convert to lowercase for comparison
//         var currentPageLower = currentPage.toLowerCase();
//         var isCRM = crmPages.indexOf(currentPageLower) !== -1;
//         console.log('Is CRM page:', isCRM);
//         return isCRM;
//     }
    
//     return false;
// }

// function isCRMPageFromPath(path) {
//     // Define the CRM pages where shortcuts should be shown
//     var crmPages = [
//         '/app/lead',
//         '/app/opportunity', 
//         '/app/customer',
//         '/app/contact',
//         '/app/appointment'
//     ];
    
//     console.log('Checking path:', path, 'against CRM paths:', crmPages);
    
//     // Check if current path starts with any of the CRM pages
//     return crmPages.some(function(page) {
//         return path.startsWith(page);
//     }); 
// } 

// function addCustomShortcutsButton(currentRoute) {
//     // Find the navbar where we want to add the button
//     // We'll add it before the help dropdown
//     var $navbar = $('.navbar-nav');
//     var $helpDropdown = $('.dropdown-help');
    
//     console.log('Navbar found:', $navbar.length, 'Help dropdown found:', $helpDropdown.length);
    
//     if ($navbar.length && $helpDropdown.length) {
//         // Create the shortcuts button using jQuery for better compatibility
//         var $shortcutsButton = $('<li class="nav-item dropdown custom-shortcuts-button"></li>');
        
//         // Create the button element
//         var $button = $('<button class="btn-reset nav-link" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false"></button>');
//         var $span = $('<span></span>');
//         $span.html(__('Shortcuts') + '<svg class="es-icon icon-xs"><use href="#es-line-down"></use></svg>');
//         $button.append($span);
        
//         // Create the dropdown menu
//         var $dropdownMenu = $('<div class="dropdown-menu dropdown-menu-right" role="menu"></div>');
        
//         // Define all CRM menu items
//         var allMenuItems = [
//             { href: '/app/lead', icon: 'fa fa-user-plus', text: __('Leads'), route: 'lead' },
//             { href: '/app/opportunity', icon: 'fa fa-bullseye', text: __('Opportunities'), route: 'opportunity' },
//             { href: '/app/customer', icon: 'fa fa-users', text: __('Customers'), route: 'customer' },
//             { href: '/app/contact', icon: 'fa fa-address-book', text: __('Contacts'), route: 'contact' },
//             { href: '/app/appointment', icon: 'fa fa-calendar', text: __('Appointments'), route: 'appointment' }
//         ];
        
//         // Filter out the current page from shortcuts
//         var currentPageRoute = currentRoute && currentRoute.length > 1 ? currentRoute[1].toLowerCase() : '';
//         var filteredMenuItems = allMenuItems.filter(function(item) {
//             return item.route !== currentPageRoute;
//         });
        
//         console.log('Current page route:', currentPageRoute);
//         console.log('Filtered menu items:', filteredMenuItems);
        
//         // Add filtered menu items to dropdown
//         filteredMenuItems.forEach(function(item) {
//             var $menuItem = $('<a class="dropdown-item" href="' + item.href + '"></a>');
//             $menuItem.html('<i class="' + item.icon + '"></i> ' + item.text);
//             $dropdownMenu.append($menuItem);
//         });
        
//         // Assemble the button
//         $shortcutsButton.append($button);
//         $shortcutsButton.append($dropdownMenu);
        
//         // Insert the button before the help dropdown
//         $shortcutsButton.insertBefore($helpDropdown);
        
//         // Initialize dropdown functionality
//         $shortcutsButton.find('[data-toggle="dropdown"]').dropdown();
        
//         console.log('Shortcuts button added successfully');
//     } else {
//         console.log('Navbar or help dropdown not found');
//     }
// }



function setLandingPageLink__LogoHeader() {
    if (document.querySelector('.navbar-brand.navbar-home')) {
        document.querySelector('.navbar-brand.navbar-home').setAttribute('href', '/landing');
    }
}