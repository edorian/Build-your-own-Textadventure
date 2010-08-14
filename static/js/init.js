var wmd_options = {
    output: "Markdown",
    buttons: "bold italic | blockquote image | ol ul heading hr",
};

$(function () {
    $('#messages li').live('click', function () {
        $(this).slideUp(1000, function () { $(this).remove(); });
    });
});
