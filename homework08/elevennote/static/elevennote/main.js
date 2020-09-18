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
        $("#delete-note").click(function(e){
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
            e.off('click');
            const share_url = window.location.origin + '/notes/shared/'
            $.get(e.data('poload'),function(data) {
                e.popover({content: share_url + data['share_key']}).popover('show');
            });
        });
        
        // Click outside popover closes it
        $(document).on("shown.bs.popover",'[data-toggle="popover"]', function(){
            $(this).attr('someattr','1');
        });
        $(document).on("hidden.bs.popover",'[data-toggle="popover"]', function(){
            $(this).attr('someattr','0');
        });
        $(document).on('click', function (e) {
            $('[data-toggle="popover"],[data-original-title]').each(function () {
                //the 'is' for buttons that trigger popups
                //the 'has' for icons within a button that triggers a popup
                if (!$(this).is(e.target) && $(this).has(e.target).length === 0 && $('.popover').has(e.target).length === 0) {
                    if($(this).attr('someattr')=="1"){
                        $(this).popover("toggle");
                    }
                }
            });
        });
    });
    

}); })(jQuery);
