$.ajax({
  url: "http://skillhub.heroku-app.com/sync",
  dataType:"json",

})
  .done(function( data ) {
    {
      console.log( "Sample of data:", data.slice( 0, 100 ) );
    }
  });
