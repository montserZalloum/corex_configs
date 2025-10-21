/**
 * Simple Awesomebar for Landing Page
 * Uses Frappe's search API and Awesomplete for autocomplete
 */

(function() {
    'use strict';

    // Wait for DOM to be ready
    document.addEventListener('DOMContentLoaded', function() {
        const searchInput = document.querySelector('#landing-navbar-search');
        if (!searchInput) {
            console.error('[AwesomeBar] Search input not found');
            return;
        }

        // Verify Awesomplete is loaded
        if (typeof Awesomplete === 'undefined') {
            console.error('[AwesomeBar] Awesomplete library not loaded');
            return;
        }

        // Initialize Awesomplete
        const awesomplete = new Awesomplete(searchInput, {
            minChars: 2,
            maxItems: 10,
            autoFirst: true,
            filter: function() { return true; }, // Server-side filtering
            sort: false, // Keep server order
            item: function(item, input) {
                const li = document.createElement('li');
                const data = typeof item === 'object' ? item : { value: item };

                let html = `<span style="font-weight: 500;">${data.value}</span>`;
                if (data.description) {
                    html += `<br><span style="font-size: 0.85em; color: rgba(255,255,255,0.6);">${data.description}</span>`;
                }

                li.innerHTML = html;
                li.setAttribute('data-doctype', data.value);
                return li;
            }
        });

        // Debounce timer
        let searchTimeout;

        // Handle input
        searchInput.addEventListener('input', function(e) {
            const query = e.target.value.trim();

            clearTimeout(searchTimeout);

            if (query.length < 2) {
                awesomplete.list = [];
                return;
            }

            searchTimeout = setTimeout(function() {
                performSearch(query);
            }, 300);
        });

        // Perform search via API
        function performSearch(query) {
            const csrfToken = getCsrfToken();

            $.ajax({
                url: '/api/method/frappe.desk.search.search_link',
                type: 'POST',
                headers: {
                    'X-Frappe-CSRF-Token': csrfToken
                },
                data: {
                    txt: query,
                    doctype: 'DocType',
                    ignore_user_permissions: 0
                },
                success: function(response) {
                    if (response.message && response.message.length > 0) {
                        const results = response.message.map(function(item) {
                            return {
                                label: item.value,
                                value: item.value,
                                description: item.description
                            };
                        });
                        awesomplete.list = results;
                    } else {
                        awesomplete.list = [];
                    }
                },
                error: function(xhr, status, error) {
                    console.error('[AwesomeBar] Search failed:', error);
                    awesomplete.list = [];
                }
            });
        }

        // Get CSRF token
        function getCsrfToken() {
            if (window.csrf_token) {
                return window.csrf_token;
            }

            const cookies = document.cookie.split(';');
            for (let cookie of cookies) {
                const [name, value] = cookie.trim().split('=');
                if (name === 'csrf_token' || name === '_csrf_token') {
                    return decodeURIComponent(value);
                }
            }
            return '';
        }

        // Handle selection - navigate to DocType
        searchInput.addEventListener('awesomplete-selectcomplete', function(e) {
            const selected = e.text.value;
            searchInput.value = '';

            if (selected) {
                // Navigate to the DocType list view
                const url = '/app/' + selected.toLowerCase().replace(/\s+/g, '-');
                window.location.href = url;
            }
        });

        // Keyboard shortcut: Ctrl/Cmd + K
        document.addEventListener('keydown', function(e) {
            const isMac = /Mac|iPod|iPhone|iPad/.test(navigator.userAgent);
            const modKey = isMac ? e.metaKey : e.ctrlKey;

            if (modKey && (e.key === 'k' || e.key === 'K')) {
                e.preventDefault();
                searchInput.focus();
            }
        });

        console.log('[AwesomeBar] Initialized successfully');
    });
})();
