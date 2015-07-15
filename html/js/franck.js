$(document).ready(function() {
    $('form').submit(function(e) {
        e.preventDefault();
        
        $("#results").html('');
        
        var url = $('input[name="url"]').val();
        url = encodeURIComponent(url);
        
        $.get("http://localhost:5000/videos/"+url, function(data, status) {
            //console.log(data);
        })
        .done(function(data) {
            data.videos.sort(function(a, b) {
                return parseInt(a.id) < parseInt(b.id);
            });
            $.each(data.videos, function(index, config) {
                var v = new Video(config);
                $("#results").append(v.render());
            });
        })
        .fail(function() {
            alert("failed");
        })
        .always(function() {
            $(window).resize();
            bLazy.revalidate();
        });
    });
    
    $("a.preset").click(function(e) {
        e.preventDefault();
        e.stopPropagation();
        
        $('input[name="url"]').val($(this).attr("href"));
        $('form').submit();
    });
    
    var bLazy = new Blazy({
        offset: 200,
        success: function(element){
            setTimeout(function(){
                element.className.replace(/\bloading\b/,'');
            }, 200);
        }
    });
    
    // debug: $('form').submit();
});
