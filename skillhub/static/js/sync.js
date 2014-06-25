$.ajax({
    url: window.location.origin + "/sync/",
    dataType:"json",
    timeout: 82000,
    success: function(response) {
        $("#sync-hubot").remove();
    },
    failure: function(response) {
        $("#sync-hubot").remove();
        alert('Something failed, maybe a timeout. Sorry about that, please refresh.');
    },
    error: function(response){
        $("#sync-hubot").remove();
        alert('Something went wrong, please refresh.');
    },
})
