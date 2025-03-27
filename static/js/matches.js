$(document).ready(function() {
    alert('Hello, world!');
    });
    
//shows match count on the index page
$(document).ready(function () {
    $.ajax({
        url: "{% url 'total-matches' %}",
        method: "GET",
        dataType: "json",
        success: function (data) {
            $("#match-count").text(data.total_matches);
        },
        error: function () {
            $("#match-count").text("0");
            console.error("Failed to load match count.");
        }
    });
});

//shows possible, accepted, and pending match counts on the user profile page
$(document).ready(function () {
    $.ajax({
        url: "{% url 'user-match-counts' %}",  
        method: "GET",
        dataType: "json",
        success: function (data) {
            $("#user-possible-count").text(data.possible);
            $("#user-accepted-count").text(data.accepted);
            $("#user-pending-count").text(data.pending);
            $("#user-denied-count").text(data.denied);
        },
        error: function () {
            console.error("Failed to load user match counts.");
        }
    });
});