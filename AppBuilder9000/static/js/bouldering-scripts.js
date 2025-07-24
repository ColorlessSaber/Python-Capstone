document.getElementById("confirm-delete").addEventListener('click', () => {

    if (confirm('Are you sure you want to delete?')) {
        fetch(
            "bouldering/user-{{user.pk}}/delete-climb-log-{{climb_log.pk}}/",
            {
                method: "POST",
                headers: {
                    'X-CSRFToken': "{{ csrf_token }}",
                }
            }
        )
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                window.location.href = data.redirect_url;
            } else {
                alert('Something happened when trying to delete the climb log');
            }
        })
            .catch(error => {
                console.log("Error when deleting climb log", error);
                alert("An error occurred while deleting the climb log");
            })
    }
});