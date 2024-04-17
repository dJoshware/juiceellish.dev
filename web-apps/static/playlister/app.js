$(document).ready(function() {

    // Variable to store selected IDs
    var selectedIds = [];

    // Get current URL
    currentURL = window.location.href;

    $('#deleteButton').on('click', function(e) {
        e.preventDefault();
        $('#deleteModal').css('display', 'block');
    });

    $('#deleteModal .btn-secondary').on('click', function(e) {
        e.preventDefault();
        $('#deleteModal').css('display', 'none');
    });

    // 'selectAll' checkbox
    $('#selectAll').on('change', function(e) {
        e.preventDefault();
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

    // Function to add songs to a playlist
    $('.add-btn').on('click', function(e) {
        e.preventDefault();
        var song_id = $(this).val();
        var playlist_id = $(this).attr('name');
        $.getJSON(`/playlister/add_to_playlist/${playlist_id}:${song_id}`, function() {
            // do nothing
        });
        return false;
    });

    // Function to add albums to a playlist
    $('.add-album-btn').on('click', function(e) {
        e.preventDefault();
        var album_id = $(this).val();
        var playlist_id = $(this).attr('name');
        $.getJSON(`/playlister/add_album_to_playlist/${playlist_id}:${album_id}`, function() {
            // do nothing
        });
        return false;
    });

    // Collect all album and single ids
    var discography = [];

    // $('.accordion-item').each(function() {
    //     // Empty array to hold song ids
    //     var songIDs = [];
    //     // Get album id
    //     var albumID = $(this).find('.add-album-btn').val();
    //     // Loop over each song in an album and add to song array
    //     $(this).find('.add-btn').each(function() {
    //         songIDs.push($(this).val());
    //     });
    //     // Add song arrays to respective album id array
    //     albumArray[albumID] = songIDs;
    // });

    // // console.log(albumArray);


    // $('.add-album-btn').on('click', function(e) {
    //     e.preventDefault();

    //     // Empty array to hold song ids
    //     var songIDs = [];
    //     // Get album id
    //     var albumID = $(this).val();
    //     // Get playlist id
    //     var playlistID = $(this).attr('name');
    //     // Loop over each song in an album and add to song array
    //     $('.accordion-item').find('.add-btn').each(function() {
    //         songIDs.push($(this).val());
    //     });
    //     // Add songIDs array to albumID array
    //     albumArray[albumID] = songIDs;

    //     console.log(albumArray);
    //     // $.getJSON(`/playlister/add_to_playlist/${playlistID}:${albumID}`, function() {
    //         // do nothing
    //     // });
    //     return false;
    // });

    // Function to remove alerts
    $('.bi-x').on('click', function(e) {
        e.preventDefault();
        $(this).parent().remove();
    });

    // Setup 'PUT' request for custom cover image
    // NEEDS WORK
    // $('#formPUT').on('submit', function(e) {
    //     e.preventDefault();

    //     // Get the value of 'cover_image' input field
    //     const coverImageInput = $('input[name="cover_image"]')[0]; // Use [0] to get the DOM element
    //     const coverImage = coverImageInput.files[0];

    //     // Create FormData object and append the file to it
    //     const formData = new FormData();
    //     formData.append('cover_image', coverImage);

    //     // Grab playlist id from DOM
    //     var playlist_id = $('input[name="playlistId"]').val();

    //     // Perform a PUT request using $.ajax
    //     $.ajax({
    //         url: `https://api.spotify.com/v1/playlists/${playlist_id}/images`,
    //         type: 'PUT',
    //         headers: ,
    //         data: formData,
    //         processData: false, // Prevent jQuery from processing the data
    //         contentType: false, // Prevent jQuery from setting contentType
    //         success: function (data, textStatus, jqXHR) {
    //             console.log('PUT request successful');
    //         },
    //         error: function (jqXHR, textStatus, errorThrown) {
    //             console.error('PUT request failed');
    //         }
    //     });
    // });

});
