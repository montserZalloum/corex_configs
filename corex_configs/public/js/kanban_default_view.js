// Function to get the last created Kanban Board for a doctype
// Cache for kanban board data to prevent multiple API calls
let kanbanBoardCache = null;
let isProcessing = false;

function getLastKanbanBoard(doctype) {
    // Return cached result if available
    if (kanbanBoardCache) {
        return Promise.resolve(kanbanBoardCache);
    }
    
    // Prevent multiple simultaneous calls
    if (isProcessing) {
        return new Promise((resolve) => {
            const checkCache = () => {
                if (kanbanBoardCache) {
                    resolve(kanbanBoardCache);
                } else {
                    setTimeout(checkCache, 50);
                }
            };
            checkCache();
        });
    }
    
    isProcessing = true;
    
    return frappe.call({
        method: "frappe.client.get_list",
        args: {
            doctype: "Kanban Board",
            filters: {
                reference_doctype: doctype
            },
            fields: ["name"],
            order_by: "creation desc",
            limit: 1
        }
    }).then(r => {
        kanbanBoardCache = r;
        isProcessing = false;
        return r;
    }).catch(err => {
        isProcessing = false;
        throw err;
    });
}

// Function to modify lead links with the correct Kanban board name
function modifyLeadLinks() {
    const leadLinks = document.querySelectorAll('a[href="/app/lead"]');

    // Only proceed if there are links to modify and we haven't run this before on them
    if (leadLinks.length > 0) {
        getLastKanbanBoard("Lead").then(r => {
            // Check if a Kanban board was found and has a name
            if (r && r.message && r.message.length > 0) {
                const lastKanbanBoardName = r.message[0].name;
                leadLinks.forEach(link => {
                    // Check if the link hasn't already been modified
                    if (!link.href.includes('/view/kanban')) {
                        // Rewrite the link to point to the latest Kanban board
                        link.href = `/app/lead/view/kanban/${encodeURIComponent(lastKanbanBoardName)}`;
                    }
                });
            }
            // If no Kanban board is found (r.message is empty), we do nothing.
            // The links will continue to point to the default list view, which is the correct behavior.
        });
    }
}

// Debounced version of modifyLeadLinks to prevent excessive calls
let modifyLeadLinksTimeout;
function debouncedModifyLeadLinks() {
    clearTimeout(modifyLeadLinksTimeout);
    modifyLeadLinksTimeout = setTimeout(modifyLeadLinks, 200);
}

// Create an observer instance to watch for DOM changes
const observer = new MutationObserver(function(mutations) {
    let shouldProcess = false;
    mutations.forEach(function(mutation) {
        if (mutation.addedNodes.length) {
            // Check if any added nodes contain lead links
            mutation.addedNodes.forEach(node => {
                if (node.nodeType === Node.ELEMENT_NODE) {
                    if (node.querySelector && node.querySelector('a[href="/app/lead"]')) {
                        shouldProcess = true;
                    }
                }
            });
        }
    });
    
    if (shouldProcess) {
        debouncedModifyLeadLinks();
    }
});

// Start observing the entire body for added nodes and subtree modifications
observer.observe(document.body, {
    childList: true,
    subtree: true
});

// Run the function once on initial load as well
frappe.ui.form.on('Workspace', {
    refresh(frm) {
        debouncedModifyLeadLinks();
    }
});