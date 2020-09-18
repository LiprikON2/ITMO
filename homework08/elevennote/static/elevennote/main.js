(function($) { $(function() {
    // allow whole list item to note to be clickable
    $("#notes li").click(function(){
        var attr = $(this).attr('data-url');
        // For some browsers, `attr` is undefined; for others,
        // `attr` is false.  Check for both.
        if (typeof attr !== typeof undefined && attr !== false) {
            location.assign($(this).attr("data-url"));
        }
    });
    
    // add Title placeholder
    $("#id_title").attr("placeholder", "Title your note");
    
    // set sidebar height
    $('#sidebar').css("height", window.innerHeight - 165 );

    // Bootstrap Tags Input config
    $('#tag-input').tagsinput({
        tagClass: 'mr-1 badge badge-info',
        trimValue: true,
        confirmKeys: [13, 188],
        itemText: function(item) {
            // Quotes --> Nothing
            return `#${item.replace(/['"]+/g, '')}`;
          }
    });

    
    $(document).ready(function(){
        $("#delete-note-form").click(function(e){
            console.log('you are trash');
            e.preventDefault();
            if (window.confirm("Are you sure?")) {
                $("#delete-note-form").submit();
            }
        });
        
        // deletes tags from note by clicking 'x'
        $('#tag-input').on('beforeItemRemove', function(e) {
            e.preventDefault();
            return false
        });
        
        // Prevents form from being submited when adding new tag by hitting ENTER
        $('.bootstrap-tagsinput > input').focus(function(){
            //disable btn when focusing the input
            $(".submit.btn").prop('disabled', true);
        }).blur(function(){
            //enable btn when bluring the input
            $(".submit.btn").prop('disabled', false);
        });

        // Share button popover
        $('*[data-poload]').click(function() {
            var e=$(this);
            const share_url = window.location.origin + '/notes/shared/'
            $.get(e.data('poload'),function(data) {
                url = share_url + data['share_key']
                e.popover({
                    html: true,
                    title: `<span class='popover-title'>Public link</span> <span class='copy badge badge-success'>COPIED</span>`,
                    content: `<a class="badge badge-light" href="${url}">${url}</a>`,
                }).popover('show');
                copyToClipboard(url)
                setTimeout(function(){ e.popover("hide"); }, 2500);
            });
        });

    });
    
    
}); })(jQuery);


const copyToClipboard = str => {
    const el = document.createElement('textarea');
    el.value = str;
    el.setAttribute('readonly', '');
    el.style.position = 'absolute';
    el.style.left = '-9999px';
    document.body.appendChild(el);
    const selected = document.getSelection().rangeCount > 0 ? document.getSelection().getRangeAt(0) : false;
    el.select();
    document.execCommand('copy');
    document.body.removeChild(el);
    if (selected) {
        document.getSelection().removeAllRanges();
        document.getSelection().addRange(selected);
    }
};
