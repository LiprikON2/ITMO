function string_to_slug(str) {
    str = str.replace(/^\s+|\s+$/g, ''); // trim
    str = str.toLowerCase();
  
    // remove accents, swap ñ for n, etc
    var from = "àáäâèéëêìíïîòóöôùúüûñç·/_,:;";
    var to   = "aaaaeeeeiiiioooouuuunc------";
    for (var i=0, l=from.length ; i<l ; i++) {
        str = str.replace(new RegExp(from.charAt(i), 'g'), to.charAt(i));
    }

    str = str.replace(/[^a-z0-9 -]/g, '') // remove invalid chars
        .replace(/\s+/g, '-') // collapse whitespace and replace by -
        .replace(/-+/g, '-'); // collapse dashes

    return str;
}




(function($) { $(function() {
    // allow whole list item to note to be clickable
    $("#notes li").click(function(){
        location.assign($(this).attr("data-url"));
    });
    
    // add Title placeholder
    $("#id_title").attr("placeholder", "Title your note");
    
    // set sidebar height
    $('#sidebar').css("height", window.innerHeight - 55 );

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
        // $('#tag-input').on('beforeItemRemove', function(e) {
        //     e.preventDefault();
        //     // when creating new note and tags are not in db so far, prevent delete request
        //     if (window.location.pathname.includes('/new')) {
        //         return false
        //     }

        //     const url = window.location.pathname
        //     // Spaces --> Dashes; Quotes --> Nothing
        //     const slug = string_to_slug(e.item)
        //     // const slug = e.item.replace(/ /g,"-").replace(/['"]+/g, '')
            
        //     const action = `${url}${slug}/delete-tag`
            
        //     const form = $(`<form hidden action="${action}" method="post"/>`).appendTo('body')
            
        //     // csrf token for form's post request
        //     const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        //     $(`<input type="hidden" name="csrfmiddlewaretoken" value="${csrftoken}"/>`).appendTo(form)
            
        //     form.submit()
            
        // });
        
        
        // Prevents form from being submited when adding new tag by hitting ENTER
        $('.bootstrap-tagsinput > input').focus(function(){
            //disable btn when focusing the input
            $(".submit.btn").prop('disabled', true);
        }).blur(function(){
            //enable btn when bluring the input
            $(".submit.btn").prop('disabled', false);
        });
        // $('.submit.btn-group').on('mouseenter', function() {
        //     console.log('LEAVE ME ALONE');
        //     $('.bootstrap-tagsinput > input').blur()
        // });
        console.log(document.querySelectorAll('.submit.btn-group'));
        console.log($('.submit.btn-group'));
        document.querySelectorAll('.submit.btn-group').onmouseover = function() { 
            console.log('LEAVE ME ALONE');
            $('.bootstrap-tagsinput > input').blur()
        };
        

        // $('.bootstrap-tagsinput > input').focus(function(){
        //     console.log('oning');
        //     $('#main-form').on('keydown', function(event){
        //         if(event.keyCode == 13) {
        //             event.preventDefault();
        //             return false;
        //         }
        //     });

        // }).blur(function(){
        //     console.log('offing');
        //     $('main-form').off('keydown');
        // });

    });
    

}); })(jQuery);