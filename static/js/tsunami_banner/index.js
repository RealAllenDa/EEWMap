$(document).ready(function () {
    var marquee = $('#main-container');
    console.log(marquee);
    marquee.each(function () {
        var mar = $(this), indent = mar.width();
        mar.marquee = function () {
            indent--;
            mar.css('text-indent', indent);
            if (indent < -1 * mar.children('#tsunami-banner').width()) {
                indent = mar.width();
            }
        };
        mar.data('interval', setInterval(mar.marquee, 1));
    });
});