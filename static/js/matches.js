$(document).ready(function () {

    //shows possible, accepted, and pending match counts on the user profile page
    $.ajax({
        url:  '/matches/user-match-counts/',  
        method: "GET",
        dataType: "json",
        success: function (data) {
            console.log("Match counts data:", data);
            $('#possible-count').text(data.possible || 0);
            $('#accepted-count').text(data.accepted || 0);
            $('#pending-count').text(data.pending || 0);
            $('#denied-count').text(data.denied || 0);
        },
        error: function () {
            console.error("Failed to load user match counts.");
        }
    });
    
    
});

