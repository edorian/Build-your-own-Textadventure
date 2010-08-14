$(function () {
    var markdown = new Showdown.converter().makeHtml;

    /* escape html */
    var escape = function (s) {
        return s.
            replace(/&/g, '&amp;').
            replace(/</g, '&lt;').
            replace(/"/g, '&quot;').
            replace(/'/g, '&#39;').
            replace(/>/g, '&gt;');
    };
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

    var updatePreview = function () {
        var value = $(this).val();
        value = escape(value);
        html = markdown(value);
        $('.preview').html(html);
        $('.preview a').attr('href', function (i, value) {
            if (!value.match(/^#\d+$/)) {
                return '';
            }
        });
        $('.preview img').remove();
    };
    $('.editor textarea').bind('change keyup', updatePreview);
    updatePreview.call($('.editor textarea').get(0));

    $('.preview a').live('mouseenter', function () {
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
        if (!rel) return;
        $(this).attr('title', 'Linking to: <strong>' + escape(rel) + '</strong>');
        $(this).tooltip({
            position: 'bottom right'
        });
        $(this).data('tooltip').show();
        $(this).attr('title', '');
    });
});
