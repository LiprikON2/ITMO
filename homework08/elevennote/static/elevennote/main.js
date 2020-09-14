(function($) { $(function() {
    // allow whole list item to note to be clickable
    $("#notes li").click(function(){
        location.assign($(this).attr("data-url"));
    });
    
    // add Title placeholder
    $("#id_title").attr("placeholder", "Title your note");
    
    // set sidebar height
    $('#sidebar').css("height", window.innerHeight - 55 );


    $('#tag-input').tagsinput({
        tagClass: 'mr-1 badge badge-info',
        trimValue: true,
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
        // Event listener on Bootstrap Tags Input generated tags 
        // $(".bootstrap-tagsinput > span > span").click(function(e){
        //     e.preventDefault();
        //     const url = window.location.pathname
        //     const slug = e.target.parentElement.innerText // not really a slug (e.g. for FTW tag the slug is ftw_1)
        //     const action = `${url}${slug}/delete-tag`
            
        //     const form = $(`<form hidden action="${action}" method="post"/>`).appendTo('body')

        //     // csrf token for form's post request
        //     const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        //     $(`<input type="hidden" name="csrfmiddlewaretoken" value="${csrftoken}"/>`).appendTo(form)

        //     form.submit()

        // });

        $('input').on('beforeItemRemove', function(e) {
            e.preventDefault();
            const url = window.location.pathname
            // Spaces --> Dashes; Quotes --> Nothing
            const slug = e.item.replace(/ /g,"-").replace(/['"]+/g, '')
            const action = `${url}${slug}/delete-tag`

            const form = $(`<form hidden action="${action}" method="post"/>`).appendTo('body')

            // csrf token for form's post request
            const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            $(`<input type="hidden" name="csrfmiddlewaretoken" value="${csrftoken}"/>`).appendTo(form)

            form.submit()

          });


    });


}); })(jQuery);