$(document).ready(function() {

    // Variable to store selected IDs
    var selectedIds = [];

    // Get current URL
    currentURL = window.location.href;

    $('#deleteButton').on('click', function(e) {
        e.preventDefault(); // Prevent default action of link
        $('#deleteModal').css('display', 'block');
    });

    $('#deleteModal .btn-secondary').on('click', function(e) {
        e.preventDefault(); // Prevent default action of link
        $('#deleteModal').css('display', 'none');
    });

    // 'selectAll' checkbox
    $('#selectAll').on('change', function(e) {
        e.preventDefault(); // Prevent default action of link
        var checkboxes = $('input[type="checkbox"]');
        checkboxes.prop('checked', $(this).prop('checked'));
        updateSelectedIds();
    });

    // Individual checkbox
    $('input[type="checkbox"]').on('change', function() {
        updateSelectedIds();
    });

    // Function to update selectedIds array
    function updateSelectedIds() {
        selectedIds = [];

        $('input[type="checkbox"]').each(function() {
            // Exclude checkbox with id='selectAll'
            if ($(this).attr('id') !== 'selectAll') {
                if ($(this).prop('checked')) {
                    selectedIds.push($(this).attr('name'));
                }
            }
        });

        // Check if all checkboxes are checked
        var allChecked = $('input[type="checkbox"]').not('#selectAll').length === selectedIds.length;

        // Uncheck 'select all' button if no checkboxes are checked
        $('#selectAll').prop('checked', allChecked);
        
        // Push 'selectedIds' array to HTML paragraph for app.py
        $('#hiddenList').val(selectedIds.join(','));
    }

    // Setup 'PUT' request for custom cover image
    $('formPUT').on('submit', function(e) {
        e.preventDefault() // Prevent default action of link

        // Get value of 'cover_image' input field
        const coverImage = $('[name="cover_image"]').value;

        // Perform a PUT request using the Fetch API
        fetch(currentURL, {
            method: 'PUT',
            headers: {
                'Content-Type': 'image-jpeg',
            },
            body: JSON.stringify({cover_image: coverImage})
        })
        .then(res => {
            if (res.ok) {
                console.log('PUT request successful');
            } else {
                console.error('PUT request failed');
            }
        })
        .catch(err => {
            console.error('Network error:', err);
        });
    });

});
