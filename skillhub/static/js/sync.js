$.ajax({
    url: window.location.origin + "/sync/",
    dataType:"json",
    success: function(response) {
        $("#sync-hubot").remove();
    },
    failure: function(response) {
        alert('Something went wrong please refresh.');
    }
})
