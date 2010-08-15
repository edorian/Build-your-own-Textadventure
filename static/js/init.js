var wmd_options = {
    output: "Markdown",
    buttons: "bold italic | ol ul heading hr",
};

$(function () {
    $('#messages li').live('click', function () {
        $(this).slideUp(1000, function () { $(this).remove(); });
    });

    if ($.browser.webkit) {
        var obj = $('.graph object');
        obj.attr('width', obj.parent().css('max-width'));
        obj.attr('height', obj.parent().css('max-height'));
        obj.parent().css('overflow', 'visible');
    }
});
