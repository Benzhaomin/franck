$(document).ready(function() {
    $('form').submit(function(e) {
        e.preventDefault();

        stopVideo();
        $("#results").html('<img class="loading" src="img/loading.svg"/>');

        var url = $('input[name="url"]').val();
        url = encodeURIComponent(url);

        $.get("http://localhost:8080/videos/"+url, function(data, status) {
            //console.log(data, status);
        })
        .done(function(data) {
            $("#results").html('');

            data.videos.sort(function(a, b) {
                return parseInt(a.id) < parseInt(b.id);
            });

            $.each(data.videos, function(index, config) {
                var v = new Video(config);
                $("#results").append(v.render());
            });

            $("#results").find("article:first-child").addClass("size-big");
        })
        .fail(function() {
            $("#results").html('<h2 class="error">Request failed</h2>');
        })
        .always(function() {
            bLazy.revalidate();
            $(window).resize();
        });
    });

    $("a.preset").click(function(e) {
        e.preventDefault();
        e.stopPropagation();

        $('input[name="url"]').val($(this).attr("href"));
        $('form').submit();
    });

    $("#results").off("click").on("click", "ul.sources > li > a", function(e) {
        e.preventDefault();
        e.stopPropagation();

        playVideo($(this).attr("href"));
    });

    function playVideo(src) {
        $("#player > video").attr("src", src).get(0).play();
        $("#player").show();
        $("html, body").animate({ scrollTop: 0 }, "slow");
    }

    function stopVideo() {
        $("#player > video").attr("src", '');
        $("#player").hide();
    }
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
