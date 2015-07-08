$(document).ready(function() {
    
    var timeline = null;
    
    $("body").on("click", ".timeline", function() {
        var self = $(this);
        
        if (self.attr("data-mode") == "playing") {
            pause(self);
        }
        else {
            play(self);
        }
    });
    
    /* Autoplay disabled
     * $("body").on("mouseenter", ".details", function() {
        var self = $(this);
        
        setTimeout(function() {
            if (self.is(":visible")) {
                play(self.find(".timeline"));
            }
        }, 500);
    });*/
    
    $("body").on("mouseleave", "article", function() {
        pause($(this).find(".timeline"));
    });
    
    function nextFrame($timeline) {
        var index = $timeline.attr("data-index");
        
        index++;
        var x = index % 10 * $timeline.width();
        var y = Math.floor(index / 10) * $timeline.height();
    
        $timeline.css({"background-position": "-"+x+"px -"+y+"px"});            
        $timeline.attr("data-index", index)
    }
    
    function pause($timeline) {
        clearInterval(timeline);
        timeline = null;
        $timeline.attr("data-mode", "paused");
        $timeline.removeClass("playing");
    }
    
    function play($timeline) {
        if ($timeline.attr("data-mode") == "stopped") {
            $timeline.css({"background-image": "url('"+$timeline.attr("data-timeline")+"')"});
            $timeline.css({"background-size": "1620px auto"});
            $timeline.css({"background-position": "0px 0px"});
        }
        
        timeline = setInterval(function() {
            nextFrame($timeline);
        }, 400);
        
        $timeline.attr("data-mode", "playing");
        $timeline.addClass("playing");
    }
});


    

    
