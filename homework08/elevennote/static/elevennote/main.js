(function($) { $(function() {
    // allow whole list item to note to be clickable
    $("#notes li").click(function(){
        location.assign($(this).attr("data-url"));
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
    });
    

}); })(jQuery);
