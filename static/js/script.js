$(document).ready(function() {
    $('#refresh-matches').click(function(){
        $.ajax({
            url: 'ajax/matches/pending/',  
            type: 'GET',
            dataType: 'json',
            success: function(data) {
                let matchesHtml = '';
                if(data.matches.length > 0) {
                    data.matches.forEach(function(match) {
                        
                        matchesHtml += `<div class="match-card">
                                            <p>Match ID: ${match.match_id}</p>
                                            <p>Status: pending</p>
                                        </div>`;
                    });
                } else {
                    matchesHtml = '<p>You have no pending matches yet.</p>';
                }
                $('#ajax-matches-container').html(matchesHtml);
            },
            error: function(xhr, status, error) {
                console.error('Error fetching pending matches:', error);
            }
        });
    });
});
