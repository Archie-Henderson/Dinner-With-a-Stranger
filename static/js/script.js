$(document).ready(function () {
    function fetchMatches(endpoint, containerId, statusLabel) {
        $(`#${containerId}`).html(`<p>Loading ${statusLabel} matches...</p>`);

        $.ajax({
            url: endpoint,
            type: 'GET',
            dataType: 'json',
            success: function (data) {
                let matchesHtml = '';
                if (data.matches.length > 0) {
                    data.matches.forEach(function (match) {
                        matchesHtml += `
                            <div class="match-card">
                                <p><strong>Match ID:</strong> ${match.match_id}</p>
                                <p>Status: ${statusLabel}</p>
                            </div>`;
                    });
                } else {
                    matchesHtml = `<p>You have no ${statusLabel} matches yet.</p>`;
                }
                $(`#${containerId}`).html(matchesHtml);
            },
            error: function (xhr, status, error) {
                console.error(`Error fetching ${statusLabel} matches:`, error);
                $(`#${containerId}`).html(`<p>Error loading ${statusLabel} matches. Please try again.</p>`);
            }
        });
    }

    // Event listeners for all 3 buttons
    $('#refresh-matches').click(function () {
        fetchMatches('/ajax/matches/pending/', 'ajax-matches-container', 'pending');
    });

    $('#refresh-accepted').click(function () {
        fetchMatches('/ajax/matches/accepted/', 'ajax-matches-container-accepted', 'accepted');
    });

    $('#refresh-denied').click(function () {
        fetchMatches('/ajax/matches/denied/', 'ajax-matches-container-denied', 'denied');
    });
});

