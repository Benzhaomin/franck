
function Video(data) {
    
    /* API to model binding */
    this.id = data['id'];
    this.cover = data['cover'];
    this.title = data['title'];
    this.sources = data['sources'];
    this.url = data['url'];
    this.config = data['config'];
}

Video.prototype.render = function() {
    var self = this;
    
    /* model to view binding */
    article = $('#video-template').html();
    article = article.replaceAll('{{cover}}', this.cover);
    article = article.replaceAll('{{title}}', this.title);
    article = article.replaceAll('{{url}}', this.url);
    article = article.replaceAll('{{config}}', this.config);
    
    //$(document).find('[data-binding="timeline"]').css('background-image', 'url('+this.timeline+')');
    
    $.each(["1080p", "720p", "400p", "272p"], function(index, value) {
        // try to get the video in a given format
        var item = self.sources[value];
    
        if (item != undefined) {
            article = article.replaceAll('{{'+value+'-href}}', item.file);
        }
        else {
            article = article.replaceAll('{{'+value+'-href}}', '#');
        }
    });
    
    return $(article);
};

String.prototype.replaceAll = function (find, replace) {
    var str = this;
    return str.replace(new RegExp(find.replace(/[-\/\\^$*+?.()|[\]{}]/g, '\\$&'), 'g'), replace);
};
