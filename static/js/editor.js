$(function () {
    var getLocationMarkup = function (location_id, text) {
        text = text || "";
        return '[' + text + '](#' + location_id + ')';
    };
    $('.editor .location').draggable({
        containment: '.editor',
        helper: 'clone'
    });
    $('.editor textarea').droppable({
        drop: function (event, ui) {
            var selection = $(this).getSelection();
            var rel = ui.draggable.attr('rel');
            var markup = getLocationMarkup(rel, selection.text);
            $(this).replaceSelection(markup, true);

            if (selection.length == 0) {
                $(this).setSelection(selection.start + 1);
            } else {
                $(this).setSelection(selection.start + markup.length);
            }
        }
    });

    $('.wmd-preview a').live('mouseenter', function () {
        var href = $(this).attr('href'),
            number = href.match(/^#(\d+)$/),
            rel;
        if (number) {
            rel = $('.location[rel=' + number[1] + ']');
            if (rel.length == 0) {
                rel = '#' + number[1];
            } else {
                rel = rel.text();
            }
        } else {
            rel = href;
        }
        $(this).attr('title', 'Linking to: <strong>' + rel + '</strong>');
        $(this).tooltip({
            position: 'bottom right'
        });
        $(this).data('tooltip').show();
        $(this).attr('title', '');
    });
});
