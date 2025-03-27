$(document).ready(function(){
    $("#dark-mode-toggle").click(function(event){
        event.preventDefault();  

        // Determine the current theme by checking the body's classes.
        // If the body has the 'dark' class, we consider the current theme dark.
        let currentTheme = $("body").hasClass("dark") ? "dark" : "light";
        // Toggle theme: switch to light if dark, or dark if light.
        let newTheme = (currentTheme === "dark") ? "light" : "dark";

        // Send AJAX POST request to update the theme.
        $.ajax({
            url: "/toggle_theme/",  
            type: "POST",
            dataType: "json",
            data: { "theme": newTheme },
            success: function(response) {
                if(response.status === "success") {
                    
                    $("body").removeClass("light dark").addClass(newTheme);
                    console.log("Theme updated to:", newTheme);
                } else {
                    console.error("Error updating theme:", response);
                }
            },
            error: function(xhr, status, error) {
                console.error("AJAX error updating theme:", error);
            }
        });
    });
});
