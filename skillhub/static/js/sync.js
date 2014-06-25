$.ajax({
    url: window.location.origin + "/sync/",
    dataType:"json",
    timeout: 80000,
    success: function(response) {
        $("#sync-hubot").remove();
    },
    failure: function(response) {
        alert('Something went wrong please refresh.');
    },
    error: function(response){
        console.log(response);
        alert('Something went wrong please refresh.');
    },
})
