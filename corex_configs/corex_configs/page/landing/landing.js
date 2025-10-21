frappe.pages['landing'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Workspaces',
		single_column: true
	});

	const container = $('<div class="module-cards-container"></div>').appendTo(page.main);
    

    // Call your backend function (no changes here)
    frappe.call({
        method: 'corex_configs.corex_configs.page.landing.landing.get_processed_workspaces', // This path should be correct for you
        callback: function(r) {
            container.empty(); // Clear the loading message

            const sidebar_items = r.message; // The data is now your custom sidebar_items list

            if (sidebar_items && sidebar_items.length > 0) {
                
                // --- THIS IS THE UPDATED PART ---
                sidebar_items.forEach(item => {
                    // Apply the filters from your Python logic directly here
                    // This honors the `parent_page` and `is_hidden` flags you added
                    if (item.is_hidden || item.parent_page) {
                        return; // Skip this item
                    }

                    // Map the NEW keys from your Python response to variables
                    const item_label = item.name;         // from "name": translated_display_name
                    const item_url = item.link;           // from "link": workspace_link
                    const item_icon = item.icon_name || 'fa fa-th'; // from "icon_name": page.get("icon")

                    // The card template remains the same, but uses the new variables
                    const card = $(`
						<a href="${item_url}" class="app-icon">
							<div class="icon-inner">
								<svg class="icon  icon-md" fill="currentColor" aria-hidden="true">
									<use class="" href="#icon-${item_icon}"></use>
								</svg>
							</div>
							<span class="app-label">${item_label}</span>
						</a>
                    `);
                    
                    container.append(card);
                });

            } else {
                container.html('<p>No navigation items were found.</p>');
            }
        },
        error: function(err) {
            container.empty();
            frappe.throw(err.message);
        }
    });
}