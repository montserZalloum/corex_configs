/**
 * Landing Page Awesomebar
 * Simplified clone of Frappe's Awesomebar for custom landing page
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

        let searchResults = [];

        // Initialize Awesomplete - mimicking Frappe's exact configuration
        const awesomplete = new Awesomplete(searchInput, {
            minChars: 0,
            maxItems: 99,
            autoFirst: true,
            list: [],
            filter: function(text, term) {
                return true; // Server-side filtering
            },
            data: function(item, input) {
                return {
                    label: item.index || "",
                    value: item.value
                };
            },
            item: function(item, input) {
                // Get the full item data
                const d = searchResults.find(r => r.value === item.value) || item;

                // Build the display HTML (like Frappe does)
                let html = `<span>${d.label || d.value}</span>`;

                if (d.description && d.value !== d.description) {
                    html += '<br><span class="text-muted ellipsis">' + d.description + '</span>';
                }

                const li = document.createElement('li');
                li.innerHTML = `<a style="font-weight:normal">${html}</a>`;
                li.setAttribute('data-value', d.value);

                return li;
            },
            sort: function(a, b) {
                return b.label - a.label;
            }
        });

        // Debounce timer
        let searchTimeout;
        let options = [];

        // Handle input - mimicking Frappe's behavior
        searchInput.addEventListener('input', function(e) {
            const value = e.target.value;
            const txt = value.trim().replace(/\s\s+/g, " ");

            clearTimeout(searchTimeout);

            options = [];
            searchResults = [];

            if (txt && txt.length > 1) {
                searchTimeout = setTimeout(function() {
                    performSearch(txt);
                }, 100); // Frappe uses 100ms debounce
            } else {
                awesomplete.list = [];
            }
        });

        // Focus event - show options even without typing (like Frappe)
        let autocomplete_open = false;
        searchInput.addEventListener('focus', function() {
            if (!autocomplete_open && this.value.trim().length > 1) {
                $(this).trigger('input');
            }
        });

        searchInput.addEventListener('awesomplete-open', function(e) {
            autocomplete_open = e.target;
        });

        searchInput.addEventListener('awesomplete-close', function(e) {
            autocomplete_open = false;
        });

        // Handle selection - navigate like Frappe does
        searchInput.addEventListener('awesomplete-selectcomplete', function(e) {
            const selectedValue = e.text.value;
            const selectedItem = searchResults.find(r => r.value === selectedValue);

            searchInput.value = '';
            searchInput.blur();

            if (selectedItem && selectedItem.value) {
                // Navigate to the DocType list view
                const doctype = selectedItem.value;
                const url = `/app/${doctype.toLowerCase().replace(/\s+/g, '-')}`;
                window.location.href = url;
            }
        });

        // Escape key to close
        searchInput.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                searchInput.blur();
            }
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
                        const results = response.message.map(function(item, index) {
                            return {
                                value: item.value,
                                label: item.value,
                                description: item.description,
                                type: 'DocType',
                                index: 100 - index // Higher index = more relevant (like Frappe)
                            };
                        });

                        searchResults = results;
                        awesomplete.list = deduplicate(results);
                    } else {
                        searchResults = [];
                        awesomplete.list = [];
                    }
                },
                error: function(xhr, status, error) {
                    console.error('[AwesomeBar] Search failed:', error);
                    searchResults = [];
                    awesomplete.list = [];
                }
            });
        }

        // Deduplicate results (like Frappe does)
        function deduplicate(options) {
            const out = [];
            const routes = [];

            options.forEach(function(option) {
                const key = option.value;
                if (routes.indexOf(key) === -1) {
                    out.push(option);
                    routes.push(key);
                }
            });

            return out.sort(function(a, b) {
                return b.index - a.index;
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

        // Keyboard shortcut: Ctrl/Cmd + K (like Frappe)
        document.addEventListener('keydown', function(e) {
            const isMac = /Mac|iPod|iPhone|iPad/.test(navigator.userAgent);
            const modKey = isMac ? e.metaKey : e.ctrlKey;

            if (modKey && (e.key === 'k' || e.key === 'K')) {
                e.preventDefault();
                searchInput.focus();
                searchInput.select();
            }
        });

        console.log('[AwesomeBar] Initialized successfully (Frappe-style)');
    });
})();
