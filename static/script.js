// static/script.js - Custom Frontend Interactivity for CareerHub Job Portal

document.addEventListener("DOMContentLoaded", function () {
    // 1. Auto-hide Bootstrap flash messages after 4 seconds
    const alerts = document.querySelectorAll(".alert-dismissible");
    alerts.forEach(function (alert) {
        setTimeout(function () {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 4000);
    });

    // 2. Ask for confirmation before deleting a job or user
    const deleteForms = document.querySelectorAll("form[action*='delete']");
    deleteForms.forEach(function (form) {
        form.addEventListener("submit", function (event) {
            const confirmed = confirm("Are you sure you want to delete this item? This action cannot be undone.");
            if (!confirmed) {
                event.preventDefault();
            }
        });
    });

    // 3. Show a loading spinner/text when importing jobs from the external API
    const apiForm = document.querySelector("form[action*='import-api-jobs']");
    if (apiForm) {
        apiForm.addEventListener("submit", function () {
            const btn = apiForm.querySelector("button[type='submit']");
            if (btn) {
                btn.innerHTML = "⏳ Fetching Live Jobs from API...";
                btn.classList.add("disabled");
            }
        });
    }
});