setTimeout(() => {
    frappe.call({
      method: "frappe.client.get_value",
      args: {
        doctype: "Website Settings",
        fieldname: "app_logo"
      },
      callback: function (r) {
        if (r.message && r.message.app_logo) {
          const link = document.querySelector("link[rel='icon']") || document.createElement('link');
          link.rel = 'icon';
          link.href =  "https://erpnext.conanacademy.com/files/Screen%20Shot%202025-01-03%20at%204.39.50%20PM.png"  || 'https://www.y-denka.com/favicon.ico';
          document.head.appendChild(link);
        }
      }
    });
  }, 5000); // 1-second delay
  